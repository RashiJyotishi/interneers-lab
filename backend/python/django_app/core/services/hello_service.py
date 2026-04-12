
class HelloService:
    def greet(self, name: str = None) -> str:
        if name:
            return f"Hello, {name}"
        return "Hello World"