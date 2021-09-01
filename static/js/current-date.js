// Добавляет текущую местную дату в тег с id = current_date_time_block
// <a class="nav-link" style="color: darkgray" id="current_date_time_block" ></a>

"use strict"
let date = new Date().toLocaleDateString()
document.getElementById('current_date_time_block').innerText = "Сегодня: " + date + "   ";