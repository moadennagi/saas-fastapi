import requests
import argparse
from fastapi import APIRouter


class RequestError(Exception):
    "Exception raised when response from api is not 200"
    def __init__(self, message: str = "") -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--daily',
        '-d',
        nargs='?',
        const='temperature_2m_max'
    )
    parser.add_argument('--current', '-c', type=str)
    args = parser.parse_args()
    if not args.daily:
        query = 'current_weather=true'
    else:
        query = f'daily={args.daily}&timezone=GMT'
        response = get_weather(query)
    return response


def get_weather(query: str = 'current_weather=true') -> dict:
    "Return current weather from open-meteo"

    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=34.01&longitude=-6.83&{query}')
    if response.status_code != 200:
        reason = response.json()['reason']
        raise RequestError(message=reason)
    res = response.json()
    return res


router = APIRouter(
    prefix='/weather'
)


@router.get('')
def weather() -> dict:
    return get_weather()


if __name__ == '__main__':
    main()
