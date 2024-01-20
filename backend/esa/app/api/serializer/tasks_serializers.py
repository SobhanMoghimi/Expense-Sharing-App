from rest_framework import serializers


class CreateSimpleTaskSerializer(serializers.Serializer):
    task_name = serializers.CharField(required=True)
    start_time = serializers.DateTimeField(required=True)
    end_time = serializers.DateTimeField(required=True)
    min_price = serializers.DecimalField(required=True, decimal_places=18, max_digits=36)
    max_price = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)
    randomness_percentage = serializers.IntegerField(min_value=0, required=True)
    check_price_interval = serializers.IntegerField(required=True, min_value=25)
    swap_bnb_amount = serializers.DecimalField(required=True, decimal_places=18, max_digits=36)
    is_enabled = serializers.BooleanField(required=True)


class DeleteTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField(required=True)
    # task_name = serializers.CharField(required=True)

class SimpleTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    task_name = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    is_enabled = serializers.BooleanField()
    check_price_interval = serializers.IntegerField()
    kwargs = serializers.CharField()

class GetSimpleTasksSerializer(serializers.Serializer):
    simple_tasks = SimpleTaskSerializer(many=True)

class CreateAdvancedTaskRequestSerializer(serializers.Serializer):
    task_name = serializers.CharField(required=True)
    trading_volume = serializers.DecimalField(max_digits=36,decimal_places=18, required=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    sales_to_buy_ratio = serializers.DecimalField(max_digits =36, decimal_places=18, required=True)
    interval = serializers.IntegerField()
    trade_amount = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)
    randomness_percentage = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)
    number_of_buy_transactions = serializers.IntegerField()
    number_of_sell_transactions = serializers.IntegerField()


class UpdateSimpleTaskRequestSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)
    is_enabled = serializers.BooleanField(required=True)

class AdvancedTaskSerializer(serializers.Serializer):
    task_name = serializers.CharField(required=True)
    task_id = serializers.IntegerField()
    # trading_volume = serializers.DecimalField(max_digits=36,decimal_places=18, required=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    interval = serializers.IntegerField()
    kwargs = serializers.CharField(required=True)
    # sale_to_buy_ratio = serializers.DecimalField(max_digits=36,decimal_places=18, required=True)
    # randomness_percentage = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)


class AdvancedTasksOutputSerializer(serializers.Serializer):
    tasks = AdvancedTaskSerializer(many=True)


class CompleteAdvancedTasksRequestSerializer(serializers.Serializer):
    sale_to_purchase_ratio = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)
    trading_volume = serializers.DecimalField(max_digits=36, decimal_places=18, required=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    interval = serializers.IntegerField(required=False)
    amount_in_bnb = serializers.DecimalField(max_digits=36, decimal_places=18, required=False)


class CompleteAdvancedTasksOutputSerializer(serializers.Serializer):
    interval = serializers.IntegerField()
    amount_in_bnb = serializers.DecimalField(max_digits=36, decimal_places=18)
    number_of_sells = serializers.IntegerField()
    number_of_buys = serializers.IntegerField()
