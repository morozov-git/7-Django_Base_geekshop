// Добавляет текущую местную дату в тег с id = current_date_time_block
// <a class="nav-link" style="color: darkgray" id="current_date_time_block" ></a>

"use strict"
let date = " " + new Date().toLocaleDateString()
let calendar = document.querySelector("#current_date_time_block");
calendar.insertAdjacentHTML('afterend', date)
//document.getElementsByClassName("far fa-calendar")[0].parentNode.innerText += date;
// document.getElementById('current_date_time_block').innerText = date;
//document.getElementById('current_date_time_block').innerText = "Сегодня: " + date + "   ";