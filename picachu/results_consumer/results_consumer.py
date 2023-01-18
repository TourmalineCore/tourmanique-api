from picachu.infrastructure.rabbitmq.rabbitmq_config_provider import RabbitMQConfigProvider
from picachu.infrastructure.rabbitmq.rabbitmq_consumer import RabbitMqConsumer
from picachu.results_consumer.commands.append_results_command import AppendResultsCommand

queue_name = RabbitMQConfigProvider.get_queue_names_config().rabbitmq_results_queue_name


def process_result(message):
    AppendResultsCommand().execute(message)


if __name__ == '__main__':
    RabbitMqConsumer(
        queue_name,
        process_result,
    ).run()
