from typing import Any, Callable
import abc

class MessageBus(abc.ABC):

    @abc.abstractmethod
    def handle_rpc(self, event_name: str) -> Callable[..., Any]:
        pass

    @abc.abstractmethod
    def call_rpc(self, event_name: str, *args: Any) -> Any:
        pass

    @abc.abstractmethod
    def handle_event(self, event_name: str) -> Callable[..., Any]:
        pass

    @abc.abstractmethod
    def publish(self, event_name: str, message: Any) -> Any:
        pass

    @abc.abstractmethod
    def shutdown(self) -> Any:
        pass