import random
import streamlit as st

st.set_page_config(
    page_title="왕국전쟁: 마지막 성",
    page_icon="⚔️",
    layout="wide",
)

# -----------------------------
# 게임 설정
# -----------------------------
SIZE = 8

UNIT_TYPES = {
    "보병": {
        "icon": "⚔️",
        "hp": 100,
        "atk": 25,
        "move": 2,
        "cost": 50,
    },
    "궁수": {
        "icon": "🏹",
        "hp": 70,
        "atk": 30,
        "move": 2,
        "cost": 70,
        "range": 2,
    },
    "기사": {
        "icon": "🐎",
        "hp": 150,
        "atk": 40,
        "move": 3,
        "cost": 100,
    },
}


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def make_unit(owner, unit_type, row, col):
    data = UNIT_TYPES[unit_type]
    return {
        "owner": owner,
        "type": unit_type,
        "hp": data["hp"],
        "max_hp": data["hp"],
        "atk": data["atk"],
        "move": data["move"],
        "row": row,
        "col": col,
    }


def new_game():
    random.seed(7)

    terrain = {}
    for r in range(SIZE):
        for c in range(SIZE):
            terrain[(r, c)] = random.choice(
                ["grass", "grass", "grass", "forest", "mountain"]
            )

    # 주요 지역은 평지
    important = [
        (7, 0), (0, 7),
        (6, 1), (1, 6),
        (4, 4), (3, 3),
    ]

    for pos in important:
        terrain[pos] = "grass"

    cities = {
        (4, 4): "neutral",
        (3, 3): "neutral",
        (5, 2): "neutral",
    }

    units = [
        make_unit("player", "보병", 7, 0),
        make_unit("player", "궁수", 7, 1),
        make_unit("player", "기사", 6, 0),

        make_unit("enemy", "보병", 0, 7),
        make_unit("enemy", "궁수", 0, 6),
        make_unit("enemy", "기사", 1, 7),
    ]

    return {
        "turn": 1,
        "gold": 120,
        "enemy_gold": 100,
        "terrain": terrain,
        "cities": cities,
        "units": units,
        "selected": None,
        "message": "병력을 선택하고 이동하거나 공격하세요.",
        "game_over": False,
        "winner": None,
    }


# -----------------------------
# 상태 관리
# -----------------------------
if "game" not in st.session_state:
    st.session_state.game = new_game()

game = st.session_state.game


def get_unit_at(row, col):
    for unit in game["units"]:
        if unit["row"] == row and unit["col"] == col and unit["hp"] > 0:
            return unit
    return None


def get_player_units():
    return [
        u for u in game["units"]
        if u["owner"] == "player" and u["hp"] > 0
    ]


def get_enemy_units():
    return [
        u for u in game["units"]
        if u["owner"] == "enemy" and u["hp"] > 0
    ]


def check_victory():
    player_units = get_player_units()
    enemy_units = get_enemy_units()

    player_hq = (7, 0)
    enemy_hq = (0, 7)

    if not enemy_units:
        game["game_over"] = True
        game["winner"] = "player"
        game["message"] = "🎉 적군이 전멸했습니다. 승리!"

    if not player_units:
        game["game_over"] = True
        game["winner"] = "enemy"
        game["message"] = "💀 모든 병력이 전멸했습니다."

    # 적군이 플레이어 본진을 점령
    enemy_on_hq = get_unit_at(*player_hq)
    if enemy_on_hq and enemy_on_hq["owner"] == "enemy":
        game["game_over"] = True
        game["winner"] = "enemy"
        game["message"] = "💀 적군이 본진을 점령했습니다!"

    # 플레이어가 적 본진을 점령
    player_on_hq = get_unit_at(*enemy_hq)
    if player_on_hq and player_on_hq["owner"] == "player":
        game["game_over"] = True
        game["winner"] = "player"
        game["message"] = "🏆 적 본진을 점령했습니다. 승리!"

    return game["game_over"]


def attack(attacker, defender):
    defender["hp"] -= attacker["atk"]

    if defender["hp"] <= 0:
        game["message"] = (
            f"💥 {attacker['type']}이(가) "
            f"{defender['type']}을(를) 처치했습니다."
        )
        game["units"].remove(defender)
    else:
        game["message"] = (
            f"⚔️ {attacker['type']}이(가) "
            f"{defender['type']}에게 {attacker['atk']} 피해!"
        )


def move_unit(unit, row, col):
    target = get_unit_at(row, col)

    # 적군이 있으면 공격
    if target and target["owner"] != unit["owner"]:
        attack(unit, target)
        return

    # 아군이 있으면 이동 불가
    if target:
        game["message"] = "🚫 해당 칸에는 아군이 있습니다."
        return

    dist = distance(
        (unit["row"], unit["col"]),
        (row, col),
    )

    if dist > unit["move"]:
        game["message"] = "🚫 이동력이 부족합니다."
        return

    terrain = game["terrain"][(row, col)]

    if terrain == "mountain":
        game["message"] = "⛰️ 산악 지형에는 들어갈 수 없습니다."
        return

    unit["row"] = row
    unit["col"] = col

    # 도시 점령
    if (row, col) in game["cities"]:
        city_owner = game["cities"][(row, col)]

        if city_owner != unit["owner"]:
            game["cities"][(row, col)] = unit["owner"]
            game["message"] = "🏙️ 도시를 점령했습니다!"
        else:
            game["message"] = "🏙️ 아군 도시로 이동했습니다."
    else:
        game["message"] = f"➡️ {unit['type']} 이동 완료."


def ai_turn():
    enemies = get_enemy_units()
    players = get_player_units()

    if not enemies or not players:
        return

    # 가장 가까운 플레이어 유닛을 추적
    for enemy in enemies:
        if not get_player_units():
            break

        players = get_player_units()

        target = min(
            players,
            key=lambda p: distance(
                (enemy["row"], enemy["col"]),
                (p["row"], p["col"]),
            ),
        )

        d = distance(
            (enemy["row"], enemy["col"]),
            (target["row"], target["col"]),
        )

        # 공격
        attack_range = UNIT_TYPES[enemy["type"]].get("range", 1)

        if d <= attack_range:
            attack(enemy, target)
            continue

        # 한 칸씩 목표 방향으로 이동
        possible = []

        dr = target["row"] - enemy["row"]
        dc = target["col"] - enemy["col"]

        if dr != 0:
            possible.append(
                (enemy["row"] + (1 if dr > 0 else -1), enemy["col"])
            )

        if dc != 0:
            possible.append(
                (enemy["row"], enemy["col"] + (1 if dc > 0 else -1))
            )

        moved = False

        for nr, nc in possible:
            if not (0 <= nr < SIZE and 0 <= nc < SIZE):
                continue

            if game["terrain"][(nr, nc)] == "mountain":
                continue

            occupied = get_unit_at(nr, nc)

            if occupied:
                if occupied["owner"] == "player":
                    attack(enemy, occupied)
                    moved = True
                    break
                continue

            enemy["row"] = nr
            enemy["col"] = nc
            moved = True
            break

        if not moved:
            continue


def end_turn():
    if game["game_over"]:
        return

    # 도시 수입
    player_cities = sum(
        1
        for owner in game["cities"].values()
        if owner == "player"
    )

    enemy_cities = sum(
        1
        for owner in game["cities"].values()
        if owner == "enemy"
    )

    game["gold"] += 30 + player_cities * 25
    game["enemy_gold"] += 25 + enemy_cities * 20

    # AI 행동
    ai_turn()

    game["turn"] += 1
    game["selected"] = None

    check_victory()


def recruit(unit_type):
    if game["game_over"]:
        return

    cost = UNIT_TYPES[unit_type]["cost"]

    if game["gold"] < cost:
        game["message"] = "💰 골드가 부족합니다."
        return

    # 본진 주변의 빈칸 탐색
    spawn_positions = [
        (7, 1),
        (6, 0),
        (6, 1),
        (7, 2),
    ]

    spawn = None

    for pos in spawn_positions:
        if get_unit_at(*pos) is None:
            spawn = pos
            break

    if spawn is None:
        game["message"] = "🚫 본진 주변에 빈 공간이 없습니다."
        return

    game["gold"] -= cost

    game["units"].append(
        make_unit(
            "player",
            unit_type,
            spawn[0],
            spawn[1],
        )
    )

    game["message"] = f"🪖 {unit_type}을(를) 생산했습니다."


# -----------------------------
# UI
# -----------------------------
st.title("⚔️ 왕국전쟁: 마지막 성")
st.caption("턴제 전략 전쟁 — 적 본진을 점령하거나 적군을 전멸시키세요.")

if game["game_over"]:
    if game["winner"] == "player":
        st.success("🏆 승리했습니다!")
    else:
        st.error("💀 패배했습니다.")

    if st.button("🔄 새 게임", use_container_width=True):
        st.session_state.game = new_game()
        st.rerun()

    st.stop()


# 상단 정보
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("턴", game["turn"])

with col2:
    st.metric("💰 골드", game["gold"])

with col3:
    st.metric("⚔️ 내 병력", len(get_player_units()))

with col4:
    st.metric("💀 적 병력", len(get_enemy_units()))


# -----------------------------
# 게임 보드
# -----------------------------
st.subheader("🗺️ 전장")

terrain_icons = {
    "grass": "🟩",
    "forest": "🌲",
    "mountain": "⛰️",
}

for r in range(SIZE):
    cols = st.columns(SIZE)

    for c in range(SIZE):
        with cols[c]:
            unit = get_unit_at(r, c)
            city = game["cities"].get((r, c))
            icon = terrain_icons[game["terrain"][(r, c)]]

            # 본진
            if (r, c) == (7, 0):
                icon = "🏰"

            if (r, c) == (0, 7):
                icon = "🏯"

            # 도시
            if city == "player":
                icon = "🏙️"
            elif city == "enemy":
                icon = "🏚️"

            # 유닛
            if unit:
                icon = UNIT_TYPES[unit["type"]]["icon"]

            selected = game["selected"]

            if (
                selected
                and selected["row"] == r
                and selected["col"] == c
            ):
                label = f"🔵 {icon}"
            else:
                label = icon

            if st.button(
                label,
                key=f"cell_{r}_{c}",
                use_container_width=True,
            ):
                # 아무것도 선택하지 않은 경우
                if game["selected"] is None:
                    if unit and unit["owner"] == "player":
                        game["selected"] = unit
                        game["message"] = (
                            f"선택: {unit['type']} "
                            f"(HP {unit['hp']}/{unit['max_hp']})"
                        )

                else:
                    selected_unit = game["selected"]

                    # 선택한 자기 유닛을 다시 누르면 선택 해제
                    if (
                        selected_unit["row"] == r
                        and selected_unit["col"] == c
                    ):
                        game["selected"] = None

                    else:
                        move_unit(selected_unit, r, c)
                        game["selected"] = None

                st.rerun()


st.info(game["message"])


# -----------------------------
# 선택된 유닛 정보
# -----------------------------
selected = game["selected"]

if selected and selected in game["units"]:
    st.subheader("🎖️ 선택한 병력")

    a, b, c, d = st.columns(4)

    with a:
        st.write(f"**{selected['type']}**")

    with b:
        st.write(f"❤️ HP: {selected['hp']}/{selected['max_hp']}")

    with c:
        st.write(f"⚔️ 공격력: {selected['atk']}")

    with d:
        st.write(f"👣 이동력: {selected['move']}")


# -----------------------------
# 생산
# -----------------------------
st.subheader("🏭 병력 생산")

recruit_cols = st.columns(3)

for i, unit_type in enumerate(UNIT_TYPES):
    data = UNIT_TYPES[unit_type]

    with recruit_cols[i]:
        st.write(
            f"{data['icon']} **{unit_type}**  \n"
            f"HP {data['hp']} / 공격 {data['atk']} / "
            f"이동 {data['move']}  \n"
            f"가격: 💰 {data['cost']}"
        )

        if st.button(
            f"{unit_type} 생산",
            key=f"recruit_{unit_type}",
            use_container_width=True,
        ):
            recruit(unit_type)
            st.rerun()


# -----------------------------
# 턴 종료
# -----------------------------
st.divider()

left, right = st.columns([3, 1])

with left:
    st.write(
        "💡 **팁:** 도시를 점령하면 매 턴 더 많은 골드를 얻습니다. "
        "궁수는 원거리 공격이 가능합니다."
    )

with right:
    if st.button(
        "⏭️ 턴 종료",
        type="primary",
        use_container_width=True,
    ):
        end_turn()
        st.rerun()


# -----------------------------
# 규칙
# -----------------------------
with st.expander("📖 게임 규칙"):
    st.markdown(
        """
        ### 승리 조건
        - 적 본진 🏯을 점령
        - 적 병력을 모두 처치

        ### 패배 조건
        - 내 병력이 모두 전멸
        - 적군에게 본진 🏰을 점령당함

        ### 전투
        - 내 유닛을 클릭한 뒤 이동할 칸을 클릭합니다.
        - 적 유닛이 있는 칸을 클릭하면 공격합니다.
        - 궁수는 최대 2칸 거리에서 공격할 수 있습니다.

        ### 경제
        - 매 턴 기본 30골드를 얻습니다.
        - 점령한 도시 하나당 추가 25골드를 얻습니다.
        - 골드로 새로운 병력을 생산할 수 있습니다.
        """
    )
