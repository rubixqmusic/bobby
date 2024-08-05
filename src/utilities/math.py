def linear_conversion(old_value, old_min, old_max, new_min, new_max):
    return ((old_value - old_min)/(old_max - old_min)) * (new_max - new_min) + new_min