import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Space Shooter",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Space Shooter")
st.caption("← → 이동 | SPACE 발사")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: #050816;
        overflow: hidden;
        font-family: Arial, sans-serif;
    }

    #game {
        width: 100%;
        height: 600px;
        background:
            radial-gradient(circle at 20% 20%, #1e3a8a 0 1px, transparent 2px),
            radial-gradient(circle at 80% 40%, #fff 0 1px, transparent 2px),
            radial-gradient(circle at 40% 80%, #60a5fa 0 1px, transparent 2px),
            #050816;
        position: relative;
        overflow: hidden;
        border: 2px solid #334155;
        border-radius: 15px;
    }

    #player {
        position: absolute;
        bottom: 25px;
        left: 50%;
        width: 45px;
        height: 45px;
        transform: translateX(-50%);
        background: #22d3ee;
        clip-path: polygon(50% 0%, 100% 100%, 50% 75%, 0% 100%);
        box-shadow: 0 0 20px #22d3ee;
    }

    .bullet {
        position: absolute;
        width: 5px;
        height: 18px;
        background: #fde047;
        box-shadow: 0 0 10px #fde047;
        border-radius: 5px;
    }

    .enemy {
        position: absolute;
        width: 35px;
        height: 35px;
        background: #f43f5e;
        border-radius: 50%;
        box-shadow: 0 0 15px #f43f5e;
    }

    #hud {
        position: absolute;
        top: 15px;
        left: 15px;
        right: 15px;
        display: flex;
        justify-content: space-between;
        color: white;
        font-size: 20px;
        font-weight: bold;
        z-index: 10;
    }

    #message {
        position: absolute;
        inset: 0;
        display: none;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        background: rgba(0,0,0,.75);
        color: white;
        z-index: 20;
        font-size: 35px;
    }

    #restart {
        margin-top: 20px;
        padding: 12px 25px;
        border: 0;
        border-radius: 10px;
        background: #22d3ee;
        font-size: 18px;
        cursor: pointer;
    }

    #mobile {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 10px;
    }

    #mobile button {
        width: 100px;
        height: 50px;
        font-size: 20px;
        border: 0;
        border-radius: 10px;
        background: #1e293b;
        color: white;
    }
</style>
</head>

<body>

<div id="game">

    <div id="hud">
        <span>점수: <span id="score">0</span></span>
        <span>❤️ <span id="life">3</span></span>
        <span>레벨: <span id="level">1</span></span>
    </div>

    <div id="player"></div>

    <div id="message">
        <div>GAME OVER</div>
        <div style="font-size:20px">
            최종 점수: <span id="finalScore">0</span>
        </div>
        <button id="restart">다시 시작</button>
    </div>

</div>

<div id="mobile">
    <button id="left">◀</button>
    <button id="fire">🔥</button>
    <button id="right">▶</button>
</div>

<script>

const game = document.getElementById("game");
const player = document.getElementById("player");

let playerX = 50;
let score = 0;
let life = 3;
let level = 1;
let bullets = [];
let enemies = [];
let keys = {};
let gameOver = false;

document.addEventListener("keydown", e => {
    keys[e.code] = true;

    if (e.code === "Space") {
        e.preventDefault();
        shoot();
    }

    if (e.code === "KeyR" && gameOver) {
        restart();
    }
});

document.addEventListener("keyup", e => {
    keys[e.code] = false;
});

function shoot() {

    if (gameOver) return;

    const bullet = document.createElement("div");
    bullet.className = "bullet";

    bullet.style.left =
        `calc(${playerX}% - 2px)`;

    bullet.style.bottom = "70px";

    game.appendChild(bullet);

    bullets.push({
        el: bullet,
        x: playerX,
        y: 70
    });
}

function spawnEnemy() {

    if (gameOver) return;

    const enemy = document.createElement("div");
    enemy.className = "enemy";

    const x = Math.random() * 92 + 4;

    enemy.style.left = `calc(${x}% - 17px)`;
    enemy.style.top = "-40px";

    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x: x,
        y: -40,
        speed: 1.2 + level * 0.3
    });
}

function collision(a, b) {

    return Math.abs(a.x - b.x) < 5 &&
           Math.abs(a.y - b.y) < 35;
}

function update() {

    if (gameOver) return;

    // 이동
    if (keys["ArrowLeft"] || keys["KeyA"]) {
        playerX -= 0.8;
    }

    if (keys["ArrowRight"] || keys["KeyD"]) {
        playerX += 0.8;
    }

    playerX = Math.max(4, Math.min(96, playerX));

    player.style.left = playerX + "%";

    // 총알
    bullets.forEach((b, index) => {

        b.y += 3.5;

        b.el.style.bottom = b.y + "px";

        if (b.y > 650) {
            b.el.remove();
            bullets.splice(index, 1);
        }
    });

    // 적
    enemies.forEach((enemy, ei) => {

        enemy.y += enemy.speed;

        enemy.el.style.top = enemy.y + "px";

        // 플레이어 충돌
        if (
            enemy.y > 500 &&
            Math.abs(enemy.x - playerX) < 6
        ) {

            enemy.el.remove();
            enemies.splice(ei, 1);

            life--;

            document.getElementById("life").textContent = life;

            if (life <= 0) {
                endGame();
            }

            return;
        }

        // 총알 충돌
        bullets.forEach((bullet, bi) => {

            const by = 600 - bullet.y;

            if (
                Math.abs(enemy.x - bullet.x) < 6 &&
                Math.abs(enemy.y - by) < 30
            ) {

                enemy.el.remove();
                bullet.el.remove();

                enemies.splice(ei, 1);
                bullets.splice(bi, 1);

                score += 10;

                document.getElementById("score")
                    .textContent = score;

                level =
                    Math.floor(score / 100) + 1;

                document.getElementById("level")
                    .textContent = level;
            }
        });

        if (enemy.y > 620) {
            enemy.el.remove();
            enemies.splice(ei, 1);

            life--;

            document.getElementById("life")
                .textContent = life;

            if (life <= 0) {
                endGame();
            }
        }
    });

    requestAnimationFrame(update);
}

function endGame() {

    gameOver = true;

    document.getElementById("finalScore")
        .textContent = score;

    document.getElementById("message")
        .style.display = "flex";
}

function restart() {

    bullets.forEach(b => b.el.remove());
    enemies.forEach(e => e.el.remove());

    bullets = [];
    enemies = [];

    score = 0;
    life = 3;
    level = 1;
    playerX = 50;
    gameOver = false;

    document.getElementById("score").textContent = "0";
    document.getElementById("life").textContent = "3";
    document.getElementById("level").textContent = "1";

    document.getElementById("message")
        .style.display = "none";

    requestAnimationFrame(update);
}

document.getElementById("restart")
    .addEventListener("click", restart);

// 모바일 버튼
document.getElementById("left")
    .addEventListener("pointerdown", () => {
        keys["ArrowLeft"] = true;
    });

document.getElementById("left")
    .addEventListener("pointerup", () => {
        keys["ArrowLeft"] = false;
    });

document.getElementById("right")
    .addEventListener("pointerdown", () => {
        keys["ArrowRight"] = true;
    });

document.getElementById("right")
    .addEventListener("pointerup", () => {
        keys["ArrowRight"] = false;
    });

document.getElementById("fire")
    .addEventListener("click", shoot);

// 적 생성
setInterval(() => {

    if (!gameOver) {
        spawnEnemy();
    }

}, 900);

update();

</script>

</body>
</html>
"""

components.html(game, height=700, scrolling=False)
