// бек на том же хосте, если открываешь через uvicorn
var API = "";

var dmg = 1;
var total = 0;
var hp = 50;
var maxHp = 50;
var loading = false;

var boss = document.getElementById("boss");
var bossArea = document.getElementById("boss-area");
var hpEl = document.getElementById("hp");
var hpText = document.getElementById("hptext");
var dmgEl = document.getElementById("dmg");
var totalEl = document.getElementById("total");
var msg = document.getElementById("msg");
var nameEl = document.getElementById("name");
var zov = document.getElementById("zov");
var flash = document.getElementById("flash");

function drawHp() {
  hpEl.style.width = (hp / maxHp * 100) + "%";
  hpText.textContent = hp + " / " + maxHp;
  dmgEl.textContent = dmg;
  totalEl.textContent = total;
}

function applyState(s) {
  hp = s.hp;
  maxHp = s.max_hp;
  dmg = s.damage_per_click;
  total = s.total_damage;
  nameEl.textContent = "конкурент на хакатоне";
  boss.classList.remove("dead");
  drawHp();
}

function popDamage(x, y, amount) {
  var el = document.createElement("span");
  el.className = "pop-dmg";
  el.textContent = "-" + amount;
  el.style.left = (x - 10) + "px";
  el.style.top = (y - 20) + "px";
  document.body.appendChild(el);
  setTimeout(function () { el.remove(); }, 600);
}

function hitFx(x, y, amount) {
  boss.classList.remove("hit");
  void boss.offsetWidth;
  boss.classList.add("hit");
  popDamage(x, y, amount);
}

function showZov() {
  zov.innerHTML = "<span>ZOV!</span>";
  zov.classList.add("show");
  flash.classList.remove("on");
  void flash.offsetWidth;
  flash.classList.add("on");
  boss.classList.add("dead");
  nameEl.textContent = "...";

  setTimeout(function () {
    zov.classList.remove("show");
    zov.innerHTML = "";
  }, 800);
}

function load() {
  fetch(API + "/api/game", { credentials: "same-origin" })
    .then(function (r) {
      if (!r.ok) throw new Error("bad status");
      return r.json();
    })
    .then(applyState)
    .catch(function () {
      msg.textContent = "запусти бек: python main.py";
    });
}

boss.onclick = function (e) {
  if (loading || hp <= 0) return;

  loading = true;
  fetch(API + "/api/game/hit", { method: "POST", credentials: "same-origin" })
    .then(function (r) {
      if (!r.ok) throw new Error("bad status");
      return r.json();
    })
    .then(function (data) {
      hitFx(e.clientX, e.clientY, data.damage);

      if (data.killed) {
        hp = 0;
        drawHp();
        showZov();

        setTimeout(function () {
          applyState(data.state);
        }, 800);
        return;
      }

      applyState(data.state);
    })
    .catch(function () {
      msg.textContent = "нет связи с сервером";
    })
    .finally(function () {
      loading = false;
    });
};

load();
