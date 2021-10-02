import numpy as np


def get_median(arr):
    return int(np.median(arr))


def get_quart75(arr):
    return int(np.quantile(arr, 0.75))


def get_brand_year_median_price(model_year_and_prices):
    return dict((model_year, get_median(model_prices)) for model_year, model_prices in model_year_and_prices.items())


def analysis_for_model(model_quart_and_median, brand_models_info, all_prices_for_brand):
    model_year_and_prices = dict()
    for model_name, model_by_years_info in brand_models_info.items():
        model_median_price_by_years = dict()
        all_prices_for_model = []

        for model_year, prices_for_one_model in model_by_years_info.items():
            all_prices_for_model += prices_for_one_model
            model_year_and_prices[model_year] = model_year_and_prices.get(model_year, []) + prices_for_one_model
            model_median_price_by_years[model_year] = get_median(prices_for_one_model)

        all_prices_for_brand += all_prices_for_model

        model_quart_and_median[model_name] = dict({'model_quart75_price': get_quart75(all_prices_for_model),
                                                   'model_median_price_by_years': model_median_price_by_years
                                                   })
    return model_year_and_prices


def analysis_of_data(data):
    brand_quart_median_models = dict()

    for brand_name, brand_models_info in data.items():
        model_quart_and_median = dict()
        all_prices_for_brand = []

        model_year_and_prices = analysis_for_model(model_quart_and_median, brand_models_info, all_prices_for_brand)

        brand_quart_median_models[brand_name] = dict({'brand_median_price_by_years': get_brand_year_median_price(model_year_and_prices),
                                                      'brand_quart75_price': get_quart75(all_prices_for_brand),
                                                      'models': model_quart_and_median
                                                      })

    return brand_quart_median_models
