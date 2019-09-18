var opts = {
    weekType: ["日", "月", "火", "水", "木", "金", "土"],
};
var ele = $('#mini-calendar');

var events = {};
var month = "";
var year = "";
var holiday = "";

function createFrame() {
    ele.append('<div class="calendar-head"><button class="btn btn-default" id="beforebutton" onclick="beforemonth()">←前月</button><p class="calendar-year-month"></p><button class="btn btn-default" id="afterbutton" onclick="aftermonth()">翌月→</button></div>');

    var outText = '<table><thead><tr>';
    for (var i = 0; i < opts.weekType.length; i++) {
        if (i === 0) {
            outText += '<th class="calendar-sun">';
        } else if (i === opts.weekType.length - 1) {
            outText += '<th class="calendar-sat">';
        } else {
            outText += '<th>';
        }

        outText += opts.weekType[i] + '</th>';
    }
    outText += '</thead><tbody></tbody></table>';
    ele.find('.calendar-head').after(outText);
}

function printType(thisYear, thisMonth) {
    ele.find('.calendar-year-month').text(thisYear + '年' + thisMonth + '月');
    var thisDate = new Date(thisYear, thisMonth - 1, 1);

    // 開始の曜日
    var startWeek = thisDate.getDay();

    var lastday = new Date(thisYear, thisMonth, 0).getDate();
    // 縦の数
    //var rowMax = Math.ceil((lastday + (startWeek+1)) / 7);
    var rowMax = Math.ceil((lastday + startWeek) / 7);

    var outText = '<tr>';
    var countDate = 1;
    // 最初の空白を出力
    for (var i = 0; i < startWeek; i++) {
        outText += '<td class="calendar-none">&nbsp;</td>';
    }
    for (var row = 0; row < rowMax; row++) {
        // 最初の行は曜日の最初から
        if (row == 0) {
            for (var col = startWeek; col < 7; col++) {
                outText += printTD(countDate, col);
                countDate++;
            }
        } else {
            // 2行目から
            outText += '<tr>';
            for (var col = 0; col < 7; col++) {
                if (lastday >= countDate) {
                    outText += printTD(countDate, col);
                } else {
                    outText += '<td class="calendar-none">&nbsp;</td>';
                }
                countDate++;
            }
        }
        outText += '</tr>';
    }
    ele.find('tbody').html(outText);

    function printTD(count, col) {
        var dayText = "";
        var tmpId = ' id="calender-id' + count + '"';
        let date = thisYear + ("0" + thisMonth).slice(-2) + ("0" + count).slice(-2);
        // 曜日classを割り当てる
        if (col === 0) tmpId += ' class="calendar-sun"';
        if (col === 6) tmpId += ' class="calendar-sat"';

        for (var i = 0; i < events.length; i++) {
            if (count == events[i].day) {
                return '<td' + tmpId + '><a href="#" onclick="click_modal_edit('+date+');"><i class="calendar-day-number">' + count + '</i><div class="calendar-labels">' + dayText + '</div></a></td>';
            }
        }
        // console.log(events);
        return '<td' + tmpId + '><a href="#1111" onclick="click_modal_button('+date+');"><i class="calendar-day-number">' + count + '</i><div class="calendar-labels">' + dayText + '</div></a></td>';


    }



    //今日の日付をマーク
    var toDay = new Date();
    if (thisYear === toDay.getFullYear()) {
        if (thisMonth === (toDay.getMonth() + 1)) {
            var dateID = 'calender-id' + toDay.getDate();
            ele.find('#' + dateID).addClass('calendar-today');
        }
    }
}

function setEvent() {
    for (var i = 0; i < events.length; i++) {
        var dateID = 'calender-id' + events[i].day;
        var getText = $('<textarea>' + events[i].title + '</textarea>');
        // typeがある場合classを付与
        var type = "";
        if (events[i].type) {
            type = '-' + events[i].type;
        }
        ele.find('#' + dateID + ' .calendar-labels').append('<span class="calender-label' + type + '">' + getText.val() + '</span>');

    }

    // 休日
    for (var i = 0; i < holiday.length; i++) {
        ele.find('#calender-id' + holiday[i]).addClass('calendar-holiday');
    }
}

function loadData(thisyear, thismonth) {
    $.ajax({
        url: '/update_calendar',
        type: 'post',
        data: {
            'year': thisyear,
            'month': thismonth
        },
        dataType: "json",
        async: false,
        success: function (data) {
            events = data.event;
            year = data.year;
            month = data.month;
            holiday = data.holiday;
        }
    });

    this.printType(year, month);
    this.setEvent();
}

function beforemonth() {
    month -= 1
    if (month < 1) {
        year -= 1;
        month = 12;
    }
    loadData(year, month)
};

function aftermonth() {
    month += 1
    if (month > 12) {
        year += 1;
        month = 1;
    }
    loadData(year, month)
};




createFrame();
loadData(new Date().getFullYear(), new Date().getMonth() + 1);