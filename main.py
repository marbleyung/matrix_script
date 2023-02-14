import asyncio
import httpx
SOURCE_URL = 'https://raw.githubusercontent.com/koury/pymx/main/source.txt'
EXPECTED = [
    160, 150, 140, 130,
    90, 50, 10, 20,
    30, 40, 80, 120,
    110, 100, 60, 70,
]


def create_matrix(result: list[str]) -> tuple[list[list[int]], int]:
    for i in result:
        if i.strip().isdigit() is False:
            result.remove(i)
    result = [int(i.strip()) for i in result]
    sqrt = int(len(result) ** 0.5)
    matrix = [result[sqrt * i:sqrt * (i + 1)] for i in range(sqrt)]
    return matrix, sqrt


def turn_matrix(matrix: list[list[int]], sqrt: int) -> list[list[int]]:
    turned_matrix = []
    for i in range(sqrt):
        turned_matrix.append(list())
        for j in range(sqrt):
            turned_matrix[i].append(matrix[sqrt-i-1][sqrt-j-1])
    return turned_matrix


def create_list(matrix: list[list[int]]) -> list[int]:
    final_list = []
    while matrix:
        final_list += matrix.pop(0)

        if matrix and matrix[0]:
            for line in matrix:
                final_list.append(line.pop())

        if matrix:
            final_list += matrix.pop()[::-1]

        if matrix and matrix[0]:
            for line in matrix[::-1]:
                final_list.append(line.pop(0))
    return final_list


async def parse_matrix(url: str) -> list[int]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
        except Exception as e:
            raise e
    result = response.text.replace('-', '').replace('+', '').split('|')
    matrix, sqrt = create_matrix(result)
    turned_matrix = turn_matrix(matrix, sqrt)
    final_list = create_list(turned_matrix)
    return final_list


def test_parse_matrix():
    assert asyncio.run(parse_matrix(SOURCE_URL)) == EXPECTED


if __name__ == '__main__':
    test_parse_matrix()
