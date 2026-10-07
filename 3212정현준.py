import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Galaxy Strike",
    page_icon="🚀",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1000px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚀 GALAXY STRIKE")
st.caption("우주를 지키고 보스를 처치하세요!")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    margin: 0;
    background: #030712;
    color: white;
    font-family: Arial, sans-serif;
    overflow-x: hidden;
}

button {
    font-family: inherit;
}

#app {
    width: 100%;
    max-width: 900px;
    margin: auto;
}

#game {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    min-height: 480px;
    overflow: hidden;
    border-radius: 18px;
    border: 2px solid #263449;
    background:
        radial-gradient(circle at 15% 20%, rgba(59,130,246,.2), transparent 20%),
        radial-gradient(circle at 80% 70%, rgba(139,92,246,.18), transparent 25%),
        linear-gradient(180deg,#020617,#071329 50%,#030712);
    touch-action: none;
}

canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}

#hud {
    position: absolute;
    top: 12px;
    left: 12px;
    right: 12px;
    z-index: 10;
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    pointer-events: none;
}

.stat {
    background: rgba(2,6,23,.78);
    border: 1px solid rgba(148,163,184,.25);
    border-radius: 9px;
    padding: 6px 9px;
    font-size: 13px;
    font-weight: bold;
    backdrop-filter: blur(4px);
}

#bossbar {
    position: absolute;
    top: 55px;
    left: 20%;
    width: 60%;
    height: 14px;
    border: 1px solid #475569;
    background: #111827;
    border-radius: 99px;
    overflow: hidden;
    display: none;
    z-index: 11;
}

#bossfill {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,#ef4444,#f97316);
    transition: width .1s;
}

#overlay {
    position: absolute;
    inset: 0;
    z-index: 50;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(2,6,23,.82);
    backdrop-filter: blur(5px);
}

.panel {
    width: min(92%,520px);
    max-height: 90%;
    overflow-y: auto;
    padding: 24px;
    border: 1px solid #334155;
    border-radius: 18px;
    background: linear-gradient(145deg,#0f172a,#111827);
    box-shadow: 0 20px 70px rgba(0,0,0,.5);
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: 900;
    color: #67e8f9;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
}

input {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #475569;
    background: #020617;
    color: white;
    font-size: 16px;
    margin-bottom: 12px;
    outline: none;
}

.section-title {
    font-weight: bold;
    margin: 15px 0 8px;
    color: #cbd5e1;
}

.skin-grid,
.shop-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 8px;
}

.card {
    border: 1px solid #334155;
    background: #0b1220;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    color: white;
}

.card.selected {
    border-color: #22d3ee;
    background: rgba(34,211,238,.12);
}

.card.locked {
    opacity: .55;
}

.ship-preview {
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.main-btn {
    width: 100%;
    padding: 14px;
    margin-top: 10px;
    border: 0;
    border-radius: 11px;
    background: #06b6d4;
    color: #001018;
    font-size: 17px;
    font-weight: 900;
    cursor: pointer;
}

.secondary-btn {
    background: #1e293b;
    color: white;
}

.danger-btn {
    background: #dc2626;
    color: white;
}

.small {
    font-size: 12px;
    color: #94a3b8;
}

#controls {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 8px;
    margin-top: 10px;
}

.control-btn {
    min-height: 50px;
    border: 1px solid #334155;
    border-radius: 10px;
    background: #0f172a;
    color: white;
    font-size: 18px;
    font-weight: bold;
    touch-action: none;
}

.control-btn:active {
    background: #164e63;
}

#weaponBar {
    margin-top: 8px;
    display: flex;
    gap: 6px;
    overflow-x: auto;
}

.weapon {
    flex: 1;
    min-width: 90px;
    padding: 7px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: #0f172a;
    color: #cbd5e1;
    text-align: center;
    font-size: 12px;
    cursor: pointer;
}

.weapon.active {
    border-color: #22d3ee;
    color: #67e8f9;
    background: #083344;
}

.power {
    position: absolute;
    z-index: 20;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    box-shadow: 0 0 18px currentColor;
    pointer-events: none;
}

@media(max-width:600px) {
    #game {
        min-height: 420px;
    }

    .title {
        font-size: 28px;
    }

    .panel {
        padding: 16px;
    }

    .stat {
        font-size: 11px;
        padding: 5px 7px;
    }
}
</style>
</head>

<body>

<div id="app">

<div id="game">
    <canvas id="canvas"></canvas>

    <div id="hud">
        <div class="stat">👤 <span id="nameHud">PLAYER</span></div>
        <div class="stat">⭐ <span id="score">0</span></div>
        <div class="stat">🪙 <span id="coins">0</span></div>
        <div class="stat">❤️ <span id="hp">100</span></div>
        <div class="stat">🛡️ <span id="shield">0</span></div>
        <div class="stat">🔥 x<span id="combo">1</span></div>
        <div class="stat">📍 <span id="stage">1-1</span></div>
        <div class="stat">🔫 <span id="weaponHud">기본탄</span></div>
    </div>

    <div id="bossbar">
        <div id="bossfill"></div>
    </div>

    <div id="overlay">

        <div class="panel" id="menuPanel">

            <div class="title">GALAXY STRIKE</div>
            <div class="subtitle">🚀 인류 최후의 방어선</div>

            <input id="nickname" maxlength="12" placeholder="닉네임을 입력하세요">

            <div class="section-title">🚀 우주선 선택</div>

            <div class="skin-grid">

                <div class="card selected" data-skin="blue">
                    <div class="ship-preview">🚀</div>
                    <div>NEBULA</div>
                    <div class="small">무료</div>
                </div>

                <div class="card" data-skin="red">
                    <div class="ship-preview">🛸</div>
                    <div>PHANTOM</div>
                    <div class="small">100 🪙</div>
                </div>

                <div class="card" data-skin="gold">
                    <div class="ship-preview">⭐</div>
                    <div>GALAXY</div>
                    <div class="small">300 🪙</div>
                </div>

            </div>

            <div class="section-title">🛒 상점</div>

            <div class="shop-grid">

                <button class="card" id="buyDamage">
                    ⚔️ 공격력<br>
                    <span class="small">+1 / 50🪙</span>
                </button>

                <button class="card" id="buyFire">
                    ⚡ 연사속도<br>
                    <span class="small">+10% / 75🪙</span>
                </button>

                <button class="card" id="buyShield">
                    🛡️ 시작 실드<br>
                    <span class="small">+20 / 100🪙</span>
                </button>

            </div>

            <div style="text-align:center;margin-top:10px">
                🪙 보유 코인: <b id="menuCoins">0</b>
            </div>

            <button class="main-btn" id="startBtn">
                🚀 게임 시작
            </button>

            <button class="main-btn secondary-btn" id="leaderBtn">
                🏆 최고 기록
            </button>

        </div>

        <div class="panel" id="gameOverPanel" style="display:none">
            <div class="title">GAME OVER</div>

            <div style="text-align:center;font-size:20px;margin:15px">
                최종 점수<br>
                <b id="finalScore">0</b>
            </div>

            <div style="text-align:center">
                🪙 획득 코인: <b id="finalCoins">0</b><br>
                🏆 최고점수: <b id="bestScore">0</b>
            </div>

            <button class="main-btn" id="againBtn">
                🔄 다시 시작
            </button>

            <button class="main-btn secondary-btn" id="menuBtn">
                🏠 메인 메뉴
            </button>
        </div>

        <div class="panel" id="leaderPanel" style="display:none">
            <div class="title">🏆 RECORD</div>
            <div id="leaderboard"></div>

            <button class="main-btn secondary-btn" id="closeLeader">
                돌아가기
            </button>
        </div>

    </div>
</div>

<div id="weaponBar">
    <div class="weapon active" data-weapon="basic">🔫 기본탄</div>
    <div class="weapon" data-weapon="triple">🔫 3연발</div>
    <div class="weapon" data-weapon="laser">⚡ 레이저</div>
    <div class="weapon" data-weapon="missile">🚀 미사일</div>
</div>

<div id="controls">
    <button class="control-btn" id="left">◀</button>
    <button class="control-btn" id="shoot">🔥 발사</button>
    <button class="control-btn" id="pause">Ⅱ</button>
    <button class="control-btn" id="right">▶</button>
</div>

</div>

<script>
(() => {

"use strict";

/* =========================
   DOM
========================= */

const game = document.getElementById("game");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const coinsEl = document.getElementById("coins");
const hpEl = document.getElementById("hp");
const shieldEl = document.getElementById("shield");
const comboEl = document.getElementById("combo");
const stageEl = document.getElementById("stage");
const weaponHud = document.getElementById("weaponHud");
const nameHud = document.getElementById("nameHud");

const overlay = document.getElementById("overlay");
const menuPanel = document.getElementById("menuPanel");
const gameOverPanel = document.getElementById("gameOverPanel");
const leaderPanel = document.getElementById("leaderPanel");

const nickname = document.getElementById("nickname");
const menuCoins = document.getElementById("menuCoins");

/* =========================
   Canvas
========================= */

let W = 900;
let H = 560;

function resizeCanvas() {
    const rect = game.getBoundingClientRect();

    W = Math.max(400, rect.width);
    H = Math.max(420, rect.height);

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = W * dpr;
    canvas.height = H * dpr;

    ctx.setTransform(dpr,0,0,dpr,0,0);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();

/* =========================
   Persistent data
========================= */

let saved = {};

try {
    saved = JSON.parse(localStorage.getItem("galaxyStrikeSave") || "{}");
} catch(e) {
    saved = {};
}

saved.coins = Number.isFinite(saved.coins) ? saved.coins : 0;
saved.best = Number.isFinite(saved.best) ? saved.best : 0;
saved.damage = Number.isFinite(saved.damage) ? saved.damage : 1;
saved.fireRate = Number.isFinite(saved.fireRate) ? saved.fireRate : 1;
saved.startShield = Number.isFinite(saved.startShield) ? saved.startShield : 0;
saved.skins = saved.skins || {blue:true,red:false,gold:false};
saved.records = Array.isArray(saved.records) ? saved.records : [];

let playerName = "PLAYER";
let selectedSkin = "blue";

/* =========================
   Game state
========================= */

let running = false;
let paused = false;
let gameOver = false;

let score = 0;
let runCoins = 0;
let hp = 100;
let shield = 0;

let combo = 1;
let comboTimer = 0;

let stage = 1;
let section = 1;

let elapsed = 0;
let spawnTimer = 0;
let powerTimer = 0;

let fireTimer = 0;
let shake = 0;

let weapon = "basic";

let boss = null;

const player = {
    x: 450,
    y: 485,
    w: 44,
    h: 38,
    speed: 430
};

const bullets = [];
const enemies = [];
const particles = [];
const powerups = [];
const stars = [];
const meteors = [];

/* =========================
   Input
========================= */

const keys = {};

window.addEventListener("keydown", e => {

    keys[e.code] = true;

    if (e.code === "Space") {
        e.preventDefault();
        shoot();
    }

    if (e.code === "Escape" || e.code === "KeyP") {
        togglePause();
    }
});

window.addEventListener("keyup", e => {
    keys[e.code] = false;
});

/* Mobile buttons */

function holdButton(id, key) {

    const b = document.getElementById(id);

    b.addEventListener("pointerdown", e => {
        e.preventDefault();
        keys[key] = true;
    });

    ["pointerup","pointercancel","pointerleave"].forEach(ev => {
        b.addEventListener(ev, () => {
            keys[key] = false;
        });
    });
}

holdButton("left","ArrowLeft");
holdButton("right","ArrowRight");

document.getElementById("shoot").addEventListener("pointerdown", e => {
    e.preventDefault();
    shoot();
});

document.getElementById("pause").addEventListener("click", togglePause);

/* =========================
   Audio
========================= */

let audioCtx = null;

function audioInit() {
    if (!audioCtx) {
        try {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        } catch(e) {}
    }
}

function sound(freq, duration, type="square", volume=.035) {

    if (!audioCtx) return;

    try {

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = type;
        osc.frequency.value = freq;

        gain.gain.setValueAtTime(volume, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(
            .001,
            audioCtx.currentTime + duration
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + duration);

    } catch(e) {}
}

function shootSound() {
    sound(520,.06,"square",.025);
}

function explosionSound() {
    sound(90,.13,"sawtooth",.04);
}

function bossSound() {
    sound(90,.35,"sawtooth",.06);
    setTimeout(() => sound(180,.3,"square",.04),120);
}

/* =========================
   Background
========================= */

for (let i=0;i<120;i++) {

    stars.push({
        x:Math.random()*W,
        y:Math.random()*H,
        s:.4+Math.random()*2,
        speed:10+Math.random()*50
    });
}

for (let i=0;i<8;i++) {

    meteors.push({
        x:Math.random()*W,
        y:Math.random()*H,
        s:20+Math.random()*50,
        r:2+Math.random()*5
    });
}

/* =========================
   Helpers
========================= */

function rand(a,b) {
    return a + Math.random() * (b-a);
}

function clamp(v,a,b) {
    return Math.max(a,Math.min(b,v));
}

function rectHit(a,b) {

    return (
        a.x < b.x+b.w &&
        a.x+a.w > b.x &&
        a.y < b.y+b.h &&
        a.y+a.h > b.y
    );
}

function save() {

    try {
        localStorage.setItem(
            "galaxyStrikeSave",
            JSON.stringify(saved)
        );
    } catch(e) {}
}

function updateHUD() {

    scoreEl.textContent = Math.floor(score);
    coinsEl.textContent = runCoins;
    hpEl.textContent = Math.max(0,Math.floor(hp));
    shieldEl.textContent = Math.max(0,Math.floor(shield));
    comboEl.textContent = combo;
    stageEl.textContent =
        boss ? "BOSS" : `${stage}-${section}`;

    const names = {
        basic:"기본탄",
        triple:"3연발",
        laser:"레이저",
        missile:"미사일"
    };

    weaponHud.textContent = names[weapon];
    nameHud.textContent = playerName;
}

/* =========================
   Particles
========================= */

function burst(x,y,color,count=18) {

    for (let i=0;i<count;i++) {

        const angle = Math.random()*Math.PI*2;
        const speed = rand(50,260);

        particles.push({
            x:x,
            y:y,
            vx:Math.cos(angle)*speed,
            vy:Math.sin(angle)*speed,
            life:rand(.3,.8),
            max:.8,
            size:rand(2,5),
            color:color
        });
    }

    shake = Math.min(12,shake+5);
    explosionSound();
}

/* =========================
   Shooting
========================= */

function makeBullet(x,y,vx,damage,type) {

    bullets.push({
        x:x,
        y:y,
        vx:vx,
        vy:-650,
        damage:damage,
        type:type,
        life:2
    });
}

function shoot() {

    if (!running || paused || gameOver) return;

    if (fireTimer > 0) return;

    audioInit();

    const damage = saved.damage;
    const rate = .22 / saved.fireRate;

    fireTimer = rate;

    if (weapon === "basic") {

        makeBullet(
            player.x,
            player.y-20,
            0,
            damage,
            "basic"
        );

    } else if (weapon === "triple") {

        [-130,0,130].forEach(vx => {

            makeBullet(
                player.x,
                player.y-20,
                vx,
                damage*.75,
                "triple"
            );

        });

    } else if (weapon === "laser") {

        makeBullet(
            player.x,
            player.y-20,
            0,
            damage*2,
            "laser"
        );

    } else if (weapon === "missile") {

        bullets.push({
            x:player.x,
            y:player.y-20,
            vx:0,
            vy:-350,
            damage:damage*3,
            type:"missile",
            life:3
        });
    }

    shootSound();
}

/* =========================
   Enemy creation
========================= */

function spawnEnemy() {

    if (boss) return;

    const difficulty =
        1 + elapsed/45 + stage*.35;

    const r = Math.random();

    let type = "normal";

    if (r < .10) type = "fast";
    else if (r < .20) type = "tank";
    else if (r < .30) type = "suicide";
    else if (r < .42) type = "shooter";

    const data = {

        normal: {
            w:30,h:30,
            hp:2,
            speed:100,
            color:"#ef4444",
            score:10
        },

        fast: {
            w:24,h:24,
            hp:1,
            speed:230,
            color:"#f97316",
            score:20
        },

        tank: {
            w:48,h:48,
            hp:10,
            speed:55,
            color:"#a855f7",
            score:40
        },

        suicide: {
            w:34,h:34,
            hp:2,
            speed:145,
            color:"#e11d48",
            score:30
        },

        shooter: {
            w:34,h:34,
            hp:3,
            speed:75,
            color:"#14b8a6",
            score:35
        }

    }[type];

    enemies.push({

        x:rand(20,W-20),
        y:-60,

        w:data.w,
        h:data.h,

        hp:data.hp,
        maxHp:data.hp,

        speed:data.speed*difficulty,
        color:data.color,

        type:type,
        score:data.score,

        shootTimer:rand(1,3)
    });
}

/* =========================
   Enemy bullets
========================= */

function enemyShoot(e) {

    bullets.push({

        x:e.x,
        y:e.y+e.h/2,

        vx:0,
        vy:270,

        damage:12,

        enemy:true,

        life:4,

        type:"enemy"
    });
}

/* =========================
   Powerups
========================= */

function spawnPowerup(x,y) {

    const types = [
        "damage",
        "fire",
        "shield",
        "heal"
    ];

    const type =
        types[Math.floor(Math.random()*types.length)];

    const info = {

        damage:{icon:"⚔️",color:"#f97316"},
        fire:{icon:"⚡",color:"#fde047"},
        shield:{icon:"🛡️",color:"#60a5fa"},
        heal:{icon:"❤️",color:"#fb7185"}

    }[type];

    const el = document.createElement("div");

    el.className = "power";
    el.textContent = info.icon;
    el.style.color = info.color;

    game.appendChild(el);

    powerups.push({
        x:x,
        y:y,
        type:type,
        el:el
    });
}

function collectPower(p) {

    if (p.type === "damage") {

        saved.damage += 1;

    } else if (p.type === "fire") {

        saved.fireRate += .15;

    } else if (p.type === "shield") {

        shield = Math.min(100,shield+35);

    } else if (p.type === "heal") {

        hp = Math.min(100,hp+30);
    }

    burst(p.x,p.y,"#22d3ee",12);
}

/* =========================
   Boss
========================= */

function spawnBoss() {

    bossSound();

    boss = {

        x:W/2,
        y:90,

        w:170,
        h:100,

        hp:500 + stage*180,
        maxHp:500 + stage*180,

        vx:150,

        shootTimer:1
    };

    document.getElementById("bossbar").style.display = "block";
}

function bossShoot() {

    if (!boss) return;

    for (let i=-2;i<=2;i++) {

        bullets.push({

            x:boss.x+i*25,
            y:boss.y+45,

            vx:i*80,
            vy:260,

            damage:15,

            enemy:true,

            life:4,

            type:"enemy"
        });
    }
}

/* =========================
   Damage player
========================= */

function hurt(amount) {

    if (shield > 0) {

        const absorbed = Math.min(shield,amount);

        shield -= absorbed;
        amount -= absorbed;
    }

    if (amount > 0) {
        hp -= amount;
    }

    shake = 14;

    if (hp <= 0) {
        endGame();
    }
}

/* =========================
   Enemy death
========================= */

function killEnemy(e) {

    score += e.score * combo;

    runCoins += Math.max(
        1,
        Math.floor(e.score/10)
    );

    combo = Math.min(10,combo+1);
    comboTimer = 2.5;

    if (Math.random() < .15) {
        spawnPowerup(e.x,e.y);
    }

    burst(e.x,e.y,e.color,20);
}

/* =========================
   Update
========================= */

function update(dt) {

    if (!running || paused || gameOver) return;

    elapsed += dt;

    fireTimer = Math.max(0,fireTimer-dt);

    comboTimer -= dt;

    if (comboTimer <= 0) {
        combo = 1;
    }

    /* Player */

    let move = 0;

    if (keys["ArrowLeft"] || keys["KeyA"]) {
        move -= 1;
    }

    if (keys["ArrowRight"] || keys["KeyD"]) {
        move += 1;
    }

    player.x += move * player.speed * dt;

    player.x =
        clamp(player.x,25,W-25);

    /* Auto shooting while space held */

    if (keys["Space"]) {
        shoot();
    }

    /* Stage */

    const targetSection =
        Math.min(3,1+Math.floor(elapsed/30));

    section = targetSection;

    if (
        elapsed >= 90 &&
        !boss
    ) {
        spawnBoss();
    }

    /* Spawn */

    spawnTimer -= dt;

    if (!boss && spawnTimer <= 0) {

        spawnEnemy();

        const difficulty =
            Math.min(0.9,elapsed/250);

        spawnTimer =
            Math.max(.25,.85-difficulty);

    }

    /* Power spawn */

    powerTimer -= dt;

    if (powerTimer <= 0) {

        powerTimer = rand(8,14);

        if (!boss) {
            spawnPowerup(
                rand(30,W-30),
                -20
            );
        }
    }

    /* Bullets */

    for (let i=bullets.length-1;i>=0;i--) {

        const b = bullets[i];

        b.x += b.vx*dt;
        b.y += b.vy*dt;

        b.life -= dt;

        if (
            b.y < -80 ||
            b.y > H+80 ||
            b.life <= 0
        ) {

            bullets.splice(i,1);
            continue;
        }

        /* Enemy bullet */

        if (b.enemy) {

            const pbox = {
                x:player.x-22,
                y:player.y-20,
                w:44,
                h:40
            };

            const bbox = {
                x:b.x-5,
                y:b.y-8,
                w:10,
                h:16
            };

            if (rectHit(pbox,bbox)) {

                hurt(b.damage);

                bullets.splice(i,1);

                burst(
                    player.x,
                    player.y,
                    "#60a5fa",
                    8
                );
            }

            continue;
        }

        /* Boss hit */

        if (boss) {

            const bb = {
                x:boss.x-boss.w/2,
                y:boss.y-boss.h/2,
                w:boss.w,
                h:boss.h
            };

            const bx = {
                x:b.x-4,
                y:b.y-10,
                w:8,
                h:20
            };

            if (rectHit(bb,bx)) {

                boss.hp -= b.damage;

                bullets.splice(i,1);

                burst(b.x,b.y,"#facc15",4);

                if (boss.hp <= 0) {

                    score += 1000 * stage;
                    runCoins += 100;

                    burst(
                        boss.x,
                        boss.y,
                        "#f97316",
                        90
                    );

                    boss = null;

                    document.getElementById(
                        "bossbar"
                    ).style.display = "none";

                    stage++;
                    section = 1;

                    score += 500;

                    sound(180,.5,"sawtooth",.08);
                }

                continue;
            }
        }

        /* Normal enemies */

        for (let j=enemies.length-1;j>=0;j--) {

            const e = enemies[j];

            const eb = {
                x:e.x-e.w/2,
                y:e.y-e.h/2,
                w:e.w,
                h:e.h
            };

            const bb = {
                x:b.x-5,
                y:b.y-10,
                w:10,
                h:20
            };

            if (rectHit(eb,bb)) {

                e.hp -= b.damage;

                if (b.type !== "laser") {
                    bullets.splice(i,1);
                }

                burst(
                    b.x,
                    b.y,
                    e.color,
                    4
                );

                if (e.hp <= 0) {

                    killEnemy(e);
                    enemies.splice(j,1);
                }

                break;
            }
        }
    }

    /* Enemies */

    for (let i=enemies.length-1;i>=0;i--) {

        const e = enemies[i];

        e.y += e.speed*dt;

        if (e.type === "shooter") {

            e.shootTimer -= dt;

            if (e.shootTimer <= 0) {

                e.shootTimer = rand(1.3,2.5);
                enemyShoot(e);
            }
        }

        const pbox = {
            x:player.x-22,
            y:player.y-20,
            w:44,
            h:40
        };

        const ebox = {
            x:e.x-e.w/2,
            y:e.y-e.h/2,
            w:e.w,
            h:e.h
        };

        if (rectHit(pbox,ebox)) {

            if (e.type === "suicide") {
                hurt(35);
            } else {
                hurt(20);
            }

            burst(
                e.x,
                e.y,
                e.color,
                20
            );

            enemies.splice(i,1);
            continue;
        }

        if (e.y > H+70) {

            enemies.splice(i,1);

            hurt(
                e.type === "suicide"
                ? 20
                : 8
            );
        }
    }

    /* Boss */

    if (boss) {

        boss.x += boss.vx*dt;

        if (
            boss.x > W-boss.w/2 ||
            boss.x < boss.w/2
        ) {
            boss.vx *= -1;
        }

        boss.shootTimer -= dt;

        if (boss.shootTimer <= 0) {

            boss.shootTimer = .8;
            bossShoot();
        }

        document.getElementById(
            "bossfill"
        ).style.width =
            Math.max(
                0,
                boss.hp/boss.maxHp*100
            ) + "%";
    }

    /* Powerups */

    for (let i=powerups.length-1;i>=0;i--) {

        const p = powerups[i];

        p.y += 80*dt;

        p.el.style.left =
            (p.x-15) + "px";

        p.el.style.top =
            (p.y-15) + "px";

        if (
            Math.abs(p.x-player.x)<35 &&
            Math.abs(p.y-player.y)<35
        ) {

            collectPower(p);

            p.el.remove();
            powerups.splice(i,1);

            continue;
        }

        if (p.y > H+40) {

            p.el.remove();
            powerups.splice(i,1);
        }
    }

    /* Particles */

    for (let i=particles.length-1;i>=0;i--) {

        const p = particles[i];

        p.x += p.vx*dt;
        p.y += p.vy*dt;

        p.vx *= .97;
        p.vy *= .97;

        p.life -= dt;

        if (p.life <= 0) {
            particles.splice(i,1);
        }
    }

    shake *= .9;

    updateHUD();
}

/* =========================
   Draw
========================= */

function drawBackground(dt) {

    ctx.fillStyle = "#020617";
    ctx.fillRect(0,0,W,H);

    /* Stars */

    ctx.fillStyle = "#cbd5e1";

    for (const s of stars) {

        s.y += s.speed*dt;

        if (s.y > H) {
            s.y = -3;
            s.x = Math.random()*W;
        }

        ctx.globalAlpha =
            .3 + s.s*.2;

        ctx.fillRect(
            s.x,
            s.y,
            s.s,
            s.s
        );
    }

    ctx.globalAlpha = 1;

    /* Planet */

    const px = W*.84;
    const py = H*.24;

    const grad = ctx.createRadialGradient(
        px-15,py-15,5,
        px,py,65
    );

    grad.addColorStop(0,"#38bdf8");
    grad.addColorStop(1,"#172554");

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(px,py,65,0,Math.PI*2);
    ctx.fill();

    /* Meteors */

    ctx.strokeStyle = "rgba(148,163,184,.5)";
    ctx.lineWidth = 2;

    for (const m of meteors) {

        m.y += m.s*dt;

        if (m.y > H+30) {
            m.y = -30;
            m.x = Math.random()*W;
        }

        ctx.beginPath();
        ctx.moveTo(m.x,m.y);
        ctx.lineTo(
            m.x-15,
            m.y-30
        );
        ctx.stroke();
    }
}

function drawPlayer() {

    let color = "#22d3ee";

    if (selectedSkin === "red") {
        color = "#fb7185";
    }

    if (selectedSkin === "gold") {
        color = "#facc15";
    }

    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );

    ctx.fillStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = 18;

    ctx.beginPath();

    ctx.moveTo(0,-25);
    ctx.lineTo(25,20);
    ctx.lineTo(8,13);
    ctx.lineTo(0,25);
    ctx.lineTo(-8,13);
    ctx.lineTo(-25,20);
    ctx.closePath();

    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.fillStyle = "#e0f2fe";

    ctx.beginPath();
    ctx.arc(0,-5,7,0,Math.PI*2);
    ctx.fill();

    ctx.restore();
}

function drawBullet(b) {

    if (b.type === "laser") {

        ctx.fillStyle = "#facc15";
        ctx.shadowColor = "#facc15";
        ctx.shadowBlur = 15;

        ctx.fillRect(
            b.x-4,
            b.y-35,
            8,
            70
        );

        ctx.shadowBlur = 0;

        return;
    }

    if (b.type === "missile") {

        ctx.fillStyle = "#fb923c";

        ctx.beginPath();
        ctx.arc(
            b.x,
            b.y,
            7,
            0,
            Math.PI*2
        );
        ctx.fill();

        ctx.fillStyle = "#fde047";

        ctx.fillRect(
            b.x-3,
            b.y+7,
            6,
            15
        );

        return;
    }

    ctx.fillStyle = "#fde047";
    ctx.shadowColor = "#fde047";
    ctx.shadowBlur = 10;

    ctx.fillRect(
        b.x-3,
        b.y-10,
        6,
        20
    );

    ctx.shadowBlur = 0;
}

function drawEnemy(e) {

    ctx.save();

    ctx.translate(e.x,e.y);

    ctx.fillStyle = e.color;
    ctx.shadowColor = e.color;
    ctx.shadowBlur = 12;

    if (e.type === "fast") {

        ctx.beginPath();
        ctx.moveTo(0,-17);
        ctx.lineTo(15,15);
        ctx.lineTo(-15,15);
        ctx.closePath();
        ctx.fill();

    } else if (e.type === "tank") {

        ctx.fillRect(
            -24,-24,
            48,48
        );

        ctx.fillStyle = "#f5f3ff";
        ctx.fillRect(-7,-7,14,14);

    } else if (e.type === "suicide") {

        ctx.beginPath();
        ctx.arc(0,0,18,0,Math.PI*2);
        ctx.fill();

        ctx.strokeStyle = "#fecdd3";
        ctx.lineWidth = 3;

        ctx.beginPath();
        ctx.moveTo(-10,-10);
        ctx.lineTo(10,10);
        ctx.moveTo(10,-10);
        ctx.lineTo(-10,10);
        ctx.stroke();

    } else {

        ctx.beginPath();
        ctx.arc(
            0,
            0,
            e.w/2,
            0,
            Math.PI*2
        );
        ctx.fill();
    }

    ctx.shadowBlur = 0;

    /* HP bar */

    if (e.maxHp > 2) {

        ctx.fillStyle = "#111827";
        ctx.fillRect(-25,-32,50,5);

        ctx.fillStyle = "#22c55e";
        ctx.fillRect(
            -25,
            -32,
            50*(e.hp/e.maxHp),
            5
        );
    }

    ctx.restore();
}

function drawBoss() {

    if (!boss) return;

    ctx.save();

    ctx.translate(
        boss.x,
        boss.y
    );

    ctx.fillStyle = "#7c3aed";
    ctx.shadowColor = "#a855f7";
    ctx.shadowBlur = 30;

    ctx.beginPath();

    ctx.moveTo(0,-50);
    ctx.lineTo(75,-20);
    ctx.lineTo(65,35);
    ctx.lineTo(30,48);
    ctx.lineTo(0,35);
    ctx.lineTo(-30,48);
    ctx.lineTo(-65,35);
    ctx.lineTo(-75,-20);
    ctx.closePath();

    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.fillStyle = "#fef08a";

    ctx.beginPath();
    ctx.arc(0,-5,22,0,Math.PI*2);
    ctx.fill();

    ctx.fillStyle = "#111827";

    ctx.beginPath();
    ctx.arc(0,-5,10,0,Math.PI*2);
    ctx.fill();

    ctx.restore();
}

function draw(dt) {

    let sx = 0;
    let sy = 0;

    if (shake > .5) {

        sx = rand(-shake,shake);
        sy = rand(-shake,shake);
    }

    ctx.save();
    ctx.translate(sx,sy);

    drawBackground(dt);

    for (const b of bullets) {
        drawBullet(b);
    }

    for (const e of enemies) {
        drawEnemy(e);
    }

    drawBoss();
    drawPlayer();

    /* particles */

    for (const p of particles) {

        ctx.globalAlpha =
            Math.max(0,p.life/p.max);

        ctx.fillStyle = p.color;

        ctx.fillRect(
            p.x,
            p.y,
            p.size,
            p.size
        );
    }

    ctx.globalAlpha = 1;

    ctx.restore();
}

/* =========================
   Main loop
========================= */

let last = performance.now();

function loop(now) {

    const dt =
        Math.min(.033,(now-last)/1000);

    last = now;

    update(dt);
    draw(dt);

    requestAnimationFrame(loop);
}

requestAnimationFrame(loop);

/* =========================
   Pause
========================= */

function togglePause() {

    if (!running || gameOver) return;

    paused = !paused;

    if (paused) {

        overlay.style.display = "flex";
        menuPanel.style.display = "block";

        document.querySelector("#menuPanel .title")
            .textContent = "⏸ PAUSED";

        document.querySelector("#startBtn")
            .textContent = "▶ 계속하기";

    } else {

        overlay.style.display = "none";

        document.querySelector("#menuPanel .title")
            .textContent = "GALAXY STRIKE";

        document.querySelector("#startBtn")
            .textContent = "🚀 게임 시작";
    }
}

/* =========================
   Game start
========================= */

function startGame() {

    audioInit();

    if (audioCtx && audioCtx.state === "suspended") {
        audioCtx.resume();
    }

    playerName =
        nickname.value.trim() || "PLAYER";

    nameHud.textContent = playerName;

    score = 0;
    runCoins = 0;
    hp = 100;

    shield = saved.startShield;

    combo = 1;
    comboTimer = 0;

    stage = 1;
    section = 1;

    elapsed = 0;
    spawnTimer = 0;
    powerTimer = 5;
    fireTimer = 0;

    bullets.length = 0;
    enemies.length = 0;
    particles.length = 0;
    powerups.forEach(p => p.el.remove());
    powerups.length = 0;

    boss = null;

    document.getElementById(
        "bossbar"
    ).style.display = "none";

    running = true;
    paused = false;
    gameOver = false;

    overlay.style.display = "none";

    updateHUD();
}

/* =========================
   Game over
========================= */

function endGame() {

    if (gameOver) return;

    gameOver = true;
    running = false;

    saved.best =
        Math.max(saved.best,Math.floor(score));

    saved.coins += runCoins;

    saved.records.push({

        name:playerName,
        score:Math.floor(score),
        stage:stage,
        date:new Date().toLocaleDateString()
    });

    saved.records.sort(
        (a,b) => b.score-a.score
    );

    saved.records =
        saved.records.slice(0,10);

    save();

    document.getElementById(
        "finalScore"
    ).textContent = Math.floor(score);

    document.getElementById(
        "finalCoins"
    ).textContent = runCoins;

    document.getElementById(
        "bestScore"
    ).textContent = saved.best;

    menuCoins.textContent = saved.coins;

    overlay.style.display = "flex";

    menuPanel.style.display = "none";
    leaderPanel.style.display = "none";
    gameOverPanel.style.display = "block";
}

/* =========================
   Menu
========================= */

function showMenu() {

    overlay.style.display = "flex";

    menuPanel.style.display = "block";
    gameOverPanel.style.display = "none";
    leaderPanel.style.display = "none";

    document.querySelector("#menuPanel .title")
        .textContent = "GALAXY STRIKE";

    document.getElementById("startBtn")
        .textContent = "🚀 게임 시작";

    menuCoins.textContent = saved.coins;
}

function renderLeaderboard() {

    const box =
        document.getElementById("leaderboard");

    if (!saved.records.length) {

        box.innerHTML =
            '<p style="text-align:center;color:#94a3b8">아직 기록이 없습니다.</p>';

        return;
    }

    box.innerHTML = saved.records.map(
        (r,i) => `
        <div style="
            display:flex;
            justify-content:space-between;
            padding:10px;
            margin:5px 0;
            border-radius:8px;
            background:#020617;
            border:1px solid #1e293b;
        ">
            <span>${i+1}. ${escapeHtml(r.name)}</span>
            <b>${r.score.toLocaleString()} ⭐</b>
        </div>
        `
    ).join("");
}

function escapeHtml(str) {

    return String(str)
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;")
        .replaceAll("'","&#039;");
}

/* =========================
   Shop
========================= */

function buy(cost,callback) {

    if (saved.coins < cost) {

        alert("코인이 부족합니다!");

        return;
    }

    saved.coins -= cost;

    callback();

    save();

    menuCoins.textContent =
        saved.coins;
}

document.getElementById("buyDamage")
.addEventListener("click",() => {

    buy(50,() => {
        saved.damage++;
    });
});

document.getElementById("buyFire")
.addEventListener("click",() => {

    buy(75,() => {
        saved.fireRate += .1;
    });
});

document.getElementById("buyShield")
.addEventListener("click",() => {

    buy(100,() => {
        saved.startShield =
            Math.min(
                100,
                saved.startShield+20
            );
    });
});

/* =========================
   Skin selection
========================= */

document.querySelectorAll(
    "[data-skin]"
).forEach(card => {

    card.addEventListener("click",() => {

        const skin =
            card.dataset.skin;

        const cost = {
            blue:0,
            red:100,
            gold:300
        }[skin];

        if (!saved.skins[skin]) {

            if (saved.coins < cost) {

                alert(
                    `이 우주선은 ${cost} 코인이 필요합니다.`
                );

                return;
            }

            saved.coins -= cost;
            saved.skins[skin] = true;

            save();
        }

        selectedSkin = skin;

        document.querySelectorAll(
            "[data-skin]"
        ).forEach(c =>
            c.classList.remove("selected")
        );

        card.classList.add("selected");

        menuCoins.textContent =
            saved.coins;
    });
});

/* =========================
   Weapon selection
========================= */

document.querySelectorAll(
    ".weapon"
).forEach(w => {

    w.addEventListener("click",() => {

        weapon = w.dataset.weapon;

        document.querySelectorAll(
            ".weapon"
        ).forEach(x =>
            x.classList.remove("active")
        );

        w.classList.add("active");

        updateHUD();
    });
});

/* =========================
   Buttons
========================= */

document.getElementById("startBtn")
.addEventListener("click",() => {

    if (paused) {
        togglePause();
    } else {
        startGame();
    }
});

document.getElementById("againBtn")
.addEventListener(
    "click",
    startGame
);

document.getElementById("menuBtn")
.addEventListener(
    "click",
    showMenu
);

document.getElementById("leaderBtn")
.addEventListener("click",() => {

    renderLeaderboard();

    menuPanel.style.display = "none";
    gameOverPanel.style.display = "none";
    leaderPanel.style.display = "block";
});

document.getElementById("closeLeader")
.addEventListener("click",showMenu);

/* =========================
   Initial
========================= */

nickname.value = "";

menuCoins.textContent =
    saved.coins;

showMenu();
updateHUD();

})();
</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=850,
    scrolling=False,
)
