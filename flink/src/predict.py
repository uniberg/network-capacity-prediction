from pyflink.table import EnvironmentSettings, BatchTableEnvironment, DataTypes
from pyflink.table.udf import udaf

env_settings = EnvironmentSettings.new_instance().in_batch_mode().use_blink_planner().build()
t_env = BatchTableEnvironment.create(environment_settings=env_settings)

# Oct, Nov, Dez 2020 + full year 2021
FORCAST_DURATION_HOURS = (31 + 30 + 31 + 365) * 24

@udaf(input_types=[DataTypes.FLOAT(), DataTypes.FLOAT(), DataTypes.FLOAT()],
     result_type=DataTypes.ARRAY(DataTypes.VARCHAR(100)), func_type='pandas')
def predict(ts_float, throughput, capacity):
    import pandas as pd
    import json
    import logging
    from fbprophet import Prophet
    logging.info('### Predictor started!')
    ds = pd.to_datetime(ts_float, unit="s")

    df_input = pd.DataFrame({'ds': ds, 'y': throughput})

    input_size = len(df_input.index)

    # Füge Wochenend-Feature hinzu
    def is_saturday(ds):
        date = pd.to_datetime(ds)
        return 1 if date.weekday() == 5 else 0
    def is_sunday(ds):
        date = pd.to_datetime(ds)
        return 1 if date.weekday() == 6 else 0

    df_input['is_saturday'] = df_input['ds'].apply(is_saturday)
    df_input['is_sunday'] = df_input['ds'].apply(is_sunday)

    model = Prophet(
        growth='linear',
        changepoint_prior_scale=0.01,
        changepoint_range=0.80,
        # n_changepoints=0,
        interval_width=0.95,
        seasonality_mode='additive',
        daily_seasonality=True,
        weekly_seasonality=False,
        yearly_seasonality=False,
    )
    # Seems to produce better results then the built in yearly seasonality
    model.add_seasonality(name="yearly",period=365, fourier_order=1)

    # Add weekend regressor
    model.add_regressor('is_saturday')
    model.add_regressor('is_sunday')

    model.fit(df_input)

    future_df = model.make_future_dataframe(
        periods=FORCAST_DURATION_HOURS,
        freq='h',
        include_history=True
    )
    # Apply is_weekend again, to set it for future data points
    future_df['is_saturday'] = future_df['ds'].apply(is_saturday)
    future_df['is_sunday'] = future_df['ds'].apply(is_sunday)
    prediction = model.predict(future_df)

    # Calculate whether interface capacity is bigger then 50%
    # TODO: To ease the calculation the capacity is treated as a constanconstantt value
    # Use the capacity of each data point instead of the max value
    prediction.loc[:,"capacity_exceeded"] = prediction.loc[:,"yhat"] > (capacity.max() / 2)
    prediction = prediction.astype({"capacity_exceeded": int})

    rename_dict = {
        "yhat": "throughput",
        "yhat_lower": "throughput_lower",
        "yhat_upper": "throughput_upper",
    }

    output_df = prediction.astype({'ds': 'str'}).rename(columns=rename_dict, errors="raise")
    list_of_dicts = output_df.to_dict('records')
    result_string_list = [json.dumps(i) for i in list_of_dicts]

    logging.info('### Predictor ended!')
    return result_string_list

t_env.register_function("predict", predict)

source_ddl = """
    create table monitoringSource (
        ts FLOAT,
        host VARCHAR(100),
        interface VARCHAR(100),
        capacity FLOAT,
        throughput FLOAT
    ) with (
        'connector.type' = 'filesystem',
        'format.type' = 'csv',
        'connector.path' = '/opt/flink/input/generated-ws-hourly.csv'
    )
"""

sink_ddl = """
    create table predictionSink (
        host VARCHAR(100),
        interface VARCHAR(100),
        prediction_row VARCHAR(1000)
    ) with (
        'connector' = 'kafka',
        'topic' = 'prediction-out',
        'properties.bootstrap.servers' = 'kafka:9092',
        'format' = 'json'
    )
"""

t_env.execute_sql(source_ddl)
t_env.execute_sql(sink_ddl)

prediction_query = """
    INSERT INTO predictionSink
    SELECT host, interface, prediction_row FROM
        (SELECT host, interface, predict(ts, throughput, capacity) AS prediction_array FROM monitoringSource GROUP BY host, interface),
        UNNEST(prediction_array) AS A (prediction_row)
"""

result = t_env.execute_sql(prediction_query)

# Wait for the job to finish
result.get_job_client().get_job_execution_result().result()
