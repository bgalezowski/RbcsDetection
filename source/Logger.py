from termcolor import colored


class Logger:
    def ok(self, string):
        print(colored(('\n' + string), 'green'))

    def info(self, string):
        print(colored(('\n' + string), 'yellow'))

    def error(self, string):
        print(colored(('\n' + string), 'red'))
