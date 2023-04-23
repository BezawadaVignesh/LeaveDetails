let calendar = document.querySelector('.calendar')

const month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

function setDate(s){
    n = s.split("-")
    date = (new Date(n[0], Number(n[1])-1, Number(n[2])+1)).toISOString().substring(0,10)
    if(!document.getElementById('id_from_date').value){
        document.getElementById('id_from_date').value = date;

        }
    else
        document.getElementById('id_to_date').value = date;
}

isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) || (year % 100 === 0 && year % 400 ===0)
}

getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28
}

generateCalendar = (month, year) => {

    let calendar_days = calendar.querySelector('.calendar-days')
    let calendar_header_year = calendar.querySelector('#year')

    let days_of_month = [31, getFebDays(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    calendar_days.innerHTML = ''

    let currDate = new Date()
    if (month > 11 || month < 0) month = currDate.getMonth()
    if (!year) year = currDate.getFullYear()

    let curr_month = `${month_names[month]}`
    month_picker.innerHTML = curr_month
    calendar_header_year.innerHTML = year

    // get first day of month

    let first_day = new Date(year, month, 1)

    for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
        let day = document.createElement('div')
        if (i >= first_day.getDay()) {
            day.classList.add('calendar-day-hover')
            let flag = false
            let msg = 'No desc'
            for(var s in h_list){
                sd = h_list[s][0].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('h-date')
                    flag = true
                    msg = h_list[s][1]
                }
            }
            //day.innerHTML = '<div class="tooltip">'+(i - first_day.getDay() + 1)+'<span class="tooltiptext">Tooltip text</span></div>'
            if (flag){
            day.innerHTML = "<button title='"+msg+"' style='border: none;background:transparent' onclick="+
            "setDate('"+year +"-"+ (month+1)+ "-" + (i - first_day.getDay() + 1) +"') ) >"
            +(i - first_day.getDay() + 1)+"</button>"
            }
            else{
            day.innerHTML = "<button style='border: none;background:transparent' onclick="+
            "setDate('"+year +"-"+ (month+1)+ "-" + (i - first_day.getDay() + 1) +"') ) >"+
            (i - first_day.getDay() + 1)+"</button>"

            }
            day.innerHTML += `<span></span>
                            <span></span>
                            <span></span>
                            <span></span>`
            if (i - first_day.getDay() + 1 === currDate.getDate() && year === currDate.getFullYear() && month === currDate.getMonth()) {
                day.classList.add('curr-date')
            }

            for(var s in cls_list){
                sd = cls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('cl-date')
                    break
                }
            }
            for(var s in ccls_list){
                sd = ccls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('ccl-date')
                    break
                }
            }for(var s in sls_list){
                sd = sls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('sl-date')
                    break
                }
            }
            for(var s in h_cls_list){
                sd = h_cls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('h_cl-date')
                    break
                }
            }
            for(var s in h_ccls_list){
                sd = h_ccls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('h_ccl-date')
                    break
                }
            }for(var s in h_sls_list){
                sd = h_sls_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('h_sl-date')
                    break
                }
            }
            for(var s in epl_list){
                sd = epl_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('epl-date')
                    break
                }
            }
            for(var s in h_epl_list){
                sd = h_epl_list[s].split('-')
                if (i - first_day.getDay()+1  === parseInt(sd[2], 10) && year === parseInt(sd[0], 10) && month+1 === parseInt(sd[1], 10)) {
                    day.classList.add('h_epl-date')
                    break
                }
            }

        }
        calendar_days.appendChild(day)
    }
}

let month_list = calendar.querySelector('.month-list')

month_names.forEach((e, index) => {
    let month = document.createElement('div')
    month.innerHTML = `<div data-month="${index}">${e}</div>`
    month.querySelector('div').onclick = () => {
        month_list.classList.remove('show')
        curr_month.value = index
        generateCalendar(index, curr_year.value)
    }
    month_list.appendChild(month)
})

let month_picker = calendar.querySelector('#month-picker')

month_picker.onclick = () => {
    month_list.classList.add('show')
}

let currDate = new Date()

let curr_month = {value: currDate.getMonth()}
let curr_year = {value: currDate.getFullYear()}

generateCalendar(curr_month.value, curr_year.value)

document.querySelector('#prev-year').onclick = () => {
    --curr_year.value
    generateCalendar(curr_month.value, curr_year.value)
}

document.querySelector('#next-year').onclick = () => {
    ++curr_year.value
    generateCalendar(curr_month.value, curr_year.value)
}