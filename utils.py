def get_dict_from_model(model):
    model_dict = model.__dict__.copy()
    model_dict.pop("_sa_instance_state", None)

    return model_dict
