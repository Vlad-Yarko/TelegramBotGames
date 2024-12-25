from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, func, DateTime, Integer, Text, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False, unique=True)
    chat_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False, unique=True)
    date: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    callback_data: Mapped[str] = mapped_column(String(50))
    image: Mapped[str] = mapped_column(Text, nullable=False)
    rules: Mapped[str] = mapped_column(Text, nullable=False)


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.tg_id), nullable=False)
    chat_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.chat_id), nullable=False)


class StatisticRPS(Base):
    __tablename__ = 'statistic_rps'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.tg_id), nullable=False)

    name: Mapped[str] = mapped_column(String(50), default='Rock Paper Scissors')

    difficulty: Mapped[str] = mapped_column(String(20), default='easy')

    win: Mapped[int] = mapped_column(Integer, default=0)
    win_easy: Mapped[int] = mapped_column(Integer, default=0)
    win_middle: Mapped[int] = mapped_column(Integer, default=0)
    win_hard: Mapped[int] = mapped_column(Integer, default=0)

    loose: Mapped[int] = mapped_column(Integer, default=0)
    loose_easy: Mapped[int] = mapped_column(Integer, default=0)
    loose_middle: Mapped[int] = mapped_column(Integer, default=0)
    loose_hard: Mapped[int] = mapped_column(Integer, default=0)


class StatisticWords(Base):
    __tablename__ = 'statistic_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.tg_id), nullable=False)

    name: Mapped[str] = mapped_column(String(50), default='Words')

    difficulty: Mapped[str] = mapped_column(String(20), default='easy')

    win: Mapped[int] = mapped_column(Integer, default=0)
    win_easy: Mapped[int] = mapped_column(Integer, default=0)
    win_middle: Mapped[int] = mapped_column(Integer, default=0)
    win_hard: Mapped[int] = mapped_column(Integer, default=0)

    loose: Mapped[int] = mapped_column(Integer, default=0)
    loose_easy: Mapped[int] = mapped_column(Integer, default=0)
    loose_middle: Mapped[int] = mapped_column(Integer, default=0)
    loose_hard: Mapped[int] = mapped_column(Integer, default=0)


class StatisticHeadTail(Base):
    __tablename__ = 'statistic_head_tail'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.tg_id), nullable=False)

    name: Mapped[str] = mapped_column(String(50), default='Head and Tail')

    difficulty: Mapped[str] = mapped_column(String(20), default='easy')

    win: Mapped[int] = mapped_column(Integer, default=0)
    win_easy: Mapped[int] = mapped_column(Integer, default=0)
    win_middle: Mapped[int] = mapped_column(Integer, default=0)
    win_hard: Mapped[int] = mapped_column(Integer, default=0)

    loose: Mapped[int] = mapped_column(Integer, default=0)
    loose_easy: Mapped[int] = mapped_column(Integer, default=0)
    loose_middle: Mapped[int] = mapped_column(Integer, default=0)
    loose_hard: Mapped[int] = mapped_column(Integer, default=0)


class StatisticSequence(Base):
    __tablename__ = 'statistic_sequence'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey(User.tg_id), nullable=False)

    name: Mapped[str] = mapped_column(String(50), default='Math sequence')

    difficulty: Mapped[str] = mapped_column(String(20), default='easy')

    win: Mapped[int] = mapped_column(Integer, default=0)
    win_easy: Mapped[int] = mapped_column(Integer, default=0)
    win_middle: Mapped[int] = mapped_column(Integer, default=0)
    win_hard: Mapped[int] = mapped_column(Integer, default=0)

    loose: Mapped[int] = mapped_column(Integer, default=0)
    loose_easy: Mapped[int] = mapped_column(Integer, default=0)
    loose_middle: Mapped[int] = mapped_column(Integer, default=0)
    loose_hard: Mapped[int] = mapped_column(Integer, default=0)


class DataWords(Base):
    __tablename__ = 'data_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)


class DataSequence(Base):
    __tablename__ = 'data_sequence'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)
