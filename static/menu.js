$(function () {
    console.log($('#registration_error'));
    if ($('#registration_error').val() == 1) {
        alert("エラー");
    }
    $('#modal1').on('hide.bs.modal', function () {
        console.log("モーダルフェイドアウト時実行");
        let meal1 = $('#meal1');
        $('check_meal1').remove();
        meal1.empty();
        let initial_option = '<option value="">未選択</option>';
        meal1.append(initial_option);

        $('#meal_td2').remove();
        $('#meal_td3').remove();
        $('#meal_td4').remove();
        $('#meal_td5').remove();
        $('#check_meal1').empty();
        $('#check_meal2').remove();
        $('#check_meal3').remove();
        $('#check_meal4').remove();
        $('#check_meal5').remove();

    });
})

let meals = [];
$.ajax({
    url: '/get_meals',
    type: 'get',
    dataType: "json",
    async: false,
    success: function (meal) {
        meals = meal;
    }
});

function click_modal_button(_date) {
    document.getElementById('modal_button').click();
    console.log(_date);

    var date = _date;
    date = date.toString(10);
    var year = date.slice(0, 4);
    var month = date.slice(4, 6);
    var day = date.slice(6, 8);
    $('#modal_title').html(year + '年 ' + month + '月 ' + day + '日' + 'のメニュー');

    $('#date_for_register').val(date);

    
    var select = $('#meal1');
    for (let row of meals) {
        var op = document.createElement("option");
        op.value = row.id;
        op.text = row.name;
        select.append(op);
    }

}


var plus_meal = function () {
    var count = $('.meal_td').length;
    count += 1

    // 新しいtr要素を生成
    var tr_new = '<td id="meal_td' + (count) + '" class="meal_td" style="padding-right: 30px;"><select class="form-control" name="meal" id="meal' + (count) + '" onChange="changemeal(this);"><option value="">未選択</option></select></td><td id="check_meal' + (count) + '"></td>';

    document.getElementById('meal_tr' + (count)).innerHTML = tr_new;

    var select = $('#meal' + (count));
    for (let row of meals) {
        var op = document.createElement("option");
        op.value = row.id;
        op.text = row.name;
        select.append(op);
    }
}



function changemeal(obj) {
    var id = obj.id;
    var check = $('#check_' + id);
    check.empty();
    var i = obj.selectedIndex;
    var value = obj.options[i].value;
    var s_price = 0;
    var m_price = 0;
    var l_price = 0;
    for (let row of meals) {
        if (value == row.id) {
            s_price = row.s_price;
            m_price = row.m_price;
            l_price = row.l_price;
        }
    }
    if (s_price > 0) {
        check.append('&emsp;小&emsp;<input type="checkbox" name="check_meal" class="large_checkbox" value="s' + id + '" checked>&emsp;&emsp;');
    } else {
        check.append('&emsp;小&emsp;<input type="checkbox" name="check_meal" class="large_checkbox" value="s' + id + '"  disabled="disabled" >&emsp;&emsp;');
    }
    if (m_price > 0) {
        check.append('&emsp;中&emsp;<input type="checkbox" name="check_meal" class="large_checkbox" value="m' + id + '" checked>&emsp;&emsp;');
    } else {
        check.append('&emsp;中&emsp;<input type="checkbox" name="check_meal" class="large_checkbox" value="m' + id + '"  disabled="disabled" >&emsp;');
    }
    if (m_price > 0) {
        check.append('&emsp;大&emsp;<input type="checkbox" name="check_meal"  class="large_checkbox"value="l' + id + '" checked>');
    } else {
        check.append('&emsp;大&emsp;<input type="checkbox" name="check_meal" class="large_checkbox" value="l' + id + '"  disabled="disabled" >');
    }
}

