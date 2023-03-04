class RuleConditions:
    def __init__(self, rule_name, condition_value, operator_value, size_value, ext_value, date_edit_value, unit_value, actions_value, original_path, target_path, rename_value):
        self.rule_name = rule_name
        self.condition_value = condition_value
        self.operator_value = operator_value
        self.size_value = size_value
        self.ext_value = ext_value
        self.date_edit_value = date_edit_value
        self.unit_value = unit_value
        self.actions_value = actions_value
        self.original_path = original_path
        self.target_path = target_path
        self.rename_value = rename_value