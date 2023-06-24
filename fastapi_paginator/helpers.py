from sqlalchemy.sql import func
from sqlmodel import select, Session

from database import sessionDep, engine


class Paginator:
    def __init__(self, session: sessionDep, query: select, page: int, per_page: int):
        self.session = session
        self.query = query
        self.page = page
        self.per_page = per_page
        self.limit = per_page
        self.offset = (page - 1) * per_page
        # computed later
        self.number_of_pages = 0
        self.next_page = ''
        self.previous_page = ''

    async def get_response(self) -> dict:
        return {
            'count': await self._get_total_count(),
            'total_pages': self._get_number_of_pages(await self._get_total_count()),
            'page_size': self.per_page,
            'page': self.page,
            'data': [item for item in self.session.scalars(self.query.offset(self.offset).limit(self.limit))]
        }

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    async def _get_total_count(self) -> int:
        count = self.session.scalar(select(func.count()).select_from(self.query.subquery()))
        self.number_of_pages = self._get_number_of_pages(count)
        return count


async def paginate(query: select, page: int, per_page: int) -> dict:
    with Session(engine) as session:
        paginator = Paginator(session, query, page, per_page)
        return await paginator.get_response()
