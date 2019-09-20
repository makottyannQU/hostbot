$(function () {

    $('#modal2').on('hide.bs.modal', function () {
        console.log("モーダルフェイドアウト時実行2");
        for (let i = 1; i <= 5; i++) {
            $('#edit_meal_td' + i).remove();
            $('#S_stock' + i).remove();
            $('#M_stock' + i).remove();
            $('#L_stock' + i).remove();
            $('#delete_button' + i).remove();
            // $('edit_meal_tr3').empty();
        }

    });

    $('#menu_edit_form').submit(function () {
        //重複チェック
        let menu_count = Number($('#menu_count').val());
        let selected_menu = []
        for (let i = 1; i <= menu_count; i++) {
            selected_menu.push($('#edit_meal' + (i)).val());
            //未選択チェック
            if (!$('#edit_meal' + (i)).val()) {
                alert("未選択のメニューが存在します。");
                return false;
            }
            //半角英数字バリデーション
            let s_stock_val = $(`input[name="S_stock${i}"]`).val();
            let m_stock_val = $(`input[name="M_stock${i}"]`).val();
            let l_stock_val = $(`input[name="L_stock${i}"]`).val();
            if (s_stock_val.match(/[^0-9]+/)) {
                alert("在庫数には半角数字を入力してください。"); 
                return false;
            }
            if (m_stock_val.match(/[^0-9]+/)) {
                alert("在庫数には半角数字を入力してください。");
                return false;
            }
            if (l_stock_val.match(/[^0-9]+/)) {
                alert("在庫数には半角数字を入力してください。");
                return false;
            }
        }
        console.log(selected_menu);

        let duplicate_check_array = [];
        selected_menu.forEach((v) => {
            if (!duplicate_check_array.includes(v)) {
                duplicate_check_array.push(v);
            }
        });
        console.log(duplicate_check_array);

        if (selected_menu.length == duplicate_check_array.length) {
            console.log("メニュー変更開始");
            return true;
        } else {
            alert("重複しているメニューがあります。正しく入力してください。");
            return false;
        }
    })
})

function click_modal_edit(_date) {
    console.log("edit_menu モーダル");
    document.getElementById('modal_edit_button').click();
    let current_menu = []
    var date = _date;
    date = date.toString(10);
    var year = date.slice(0, 4);
    var month = date.slice(4, 6);
    var day = date.slice(6, 8);
    let menu_count = 0;

    //選択された日付に注文が入っているか確認
    let exist_order_flag = false;
    for (let i = 0; i < order_check_list.length; i++) {
        if (day == order_check_list[i]) {
            exist_order_flag = true;
        }
    }
    //
    if (exist_order_flag) {
        $('#order_flag').val(1);
    } else {
        $('#order_flag').val(0);
    }

    //モーダルに日付を埋め込み(フォームにて使用)
    $('#date_for_register_edit').val(date);

    console.log(events[0].day);
    console.log(day);
    for (let i = 0; i < events.length; i++) {
        if (events[i].day.toString().padStart(2, '0') == day) {
            current_menu.push(events[i]);
            menu_count += 1;
        }

    }
    console.log(menu_count);
    console.log(current_menu);

    //モーダルタイトル埋め込み
    $('#modal_title2').html(year + '年 ' + month + '月 ' + day + '日' + 'のメニュー');

    //menu個数埋め込み
    $('#menu_count').val(menu_count);

    //モーダル要素の作成
    for (let i = 1; i <= menu_count; i++) {
        var tr_new = '<td id="edit_meal_td' + (i) + '" class="edit_meal_td" style="padding-right: 30px;"><select class="form-control" name="edit_meal' + (i) + '" id="edit_meal' + (i) + '" onChange="changemeal(this);"><option value="">未選択</option></select></td>';
        let S_td = '<td id="S_stock' + (i) + '">\
            <div class = "input-group"><input name= "S_stock' + (i) + '" class = "form-control" value = ' + current_menu[i - 1].s_stock + '>\
            <span class = "input-group-addon">'+ current_menu[i - 1].s_orders + '</span>\
            </div>\
            </td>';
        let M_td = '<td id="M_stock' + (i) + '">\
            <div class = "input-group"><input name= "M_stock' + (i) + '" class = "form-control" value = ' + current_menu[i - 1].m_stock + '>\
            <span class = "input-group-addon">'+ current_menu[i - 1].m_orders + '</span>\
            </div>\
            </td>';
        let L_td = '<td id="L_stock' + (i) + '">\
            <div class = "input-group"><input name= "L_stock' + (i) + '" class = "form-control" value = ' + current_menu[i - 1].l_stock + '>\
            <span class = "input-group-addon">'+ current_menu[i - 1].l_orders + '</span>\
            </div>\
            </td>';
        let delete_button = '<td><button type="button" class="btn btn-danger" onclick="delete_row(this)" value = ' + i + ' id="delete_button' + (i) + '">削除</button></td>';
        //最後の行のみ削除ボタンをつける
        if (i == menu_count) {
            //注文の有無によって削除ボタンの有無を決定
            if (exist_order_flag) {
                document.getElementById('edit_meal_tr' + (i)).innerHTML = tr_new + S_td + M_td + L_td;
            } else {
                document.getElementById('edit_meal_tr' + (i)).innerHTML = tr_new + S_td + M_td + L_td + delete_button;

            }
        } else {
            document.getElementById('edit_meal_tr' + (i)).innerHTML = tr_new + S_td + M_td + L_td;
        }
        var select = $('#edit_meal' + (i));
        for (let row of meals) {
            let op = document.createElement("option");
            op.value = row.id;
            op.text = row.name;
            if (current_menu[i - 1].title == row.name) {
                op.selected = true;
            }
            select.append(op);

        }
    }
}

//メニュー編集の際、行の一番下以外を削除すると、仕様上修正が大変なので一番下のみ削除できるようにした　
function delete_row(obj) {
    $('#edit_meal_td' + obj.value).remove();
    $('#S_stock' + obj.value).remove();
    $('#M_stock' + obj.value).remove();
    $('#L_stock' + obj.value).remove();
    $('#delete_button' + obj.value).remove();
    //menu個数埋め込み
    let count = $('#menu_count').val();
    count -= 1;
    $('#menu_count').val(count);
    //削除ボタンを追加
    let temp = String(obj.value - 1);
    $('#edit_meal_tr' + temp).append('<button type="button" class="btn btn-danger" onclick="delete_row(this)" value = ' + temp + ' id="delete_button' + (temp) + '">削除</button>');

}

var plus_meal_editmode = function () {
    var count = $('.edit_meal_td').length;
    //count番目の削除ボタンの削除
    $('#delete_button' + String(count)).remove();

    count += 1
    //menu個数埋め込み
    let count_embedded = Number($('#menu_count').val());
    count_embedded += 1;
    $('#menu_count').val(count_embedded);
    count = count_embedded;

    // 新しいtr要素を生成
    var tr_new = '<td id="edit_meal_td' + (count) + '" class="edit_meal_td" style="padding-right: 30px;"><select class="form-control" name="edit_meal' + (count) + '" id="edit_meal' + (count) + '" onChange="changemeal_editmode(this);"><option value="">未選択</option></select></td>';
    let S_td = '<td id="S_stock' + (count) + '">\
     <div class = "input-group"><input name= "S_stock' + (count) + '" class = "form-control" value = 0>\
            <span class = "input-group-addon">0</span>\
            </div>\
    </td>';
    let M_td = '<td id="M_stock' + (count) + '">\
   <div class = "input-group"><input name= "M_stock' + (count) + '" class = "form-control" value = 0>\
            <span class = "input-group-addon">0</span>\
            </div>\
    </td>';
    let L_td = '<td id="L_stock' + (count) + '">\
    <div class = "input-group"><input name= "L_stock' + (count) + '" class = "form-control" value = 0>\
            <span class = "input-group-addon">0</span>\
            </div>\
    </td>';
    var order_flag = $("#order_flag").val();
    let delete_button = '<td><button type="button" class="btn btn-danger" onclick="delete_row(this)" value = ' + count + ' id="delete_button' + (count) + '">削除</button></td>'
    if (order_flag == 0) {
        document.getElementById('edit_meal_tr' + (count)).innerHTML = tr_new + S_td + M_td + L_td + delete_button;        
    } else if (order_flag == 1) {
        document.getElementById('edit_meal_tr' + (count)).innerHTML = tr_new + S_td + M_td + L_td;                
    }
    var select = $('#edit_meal' + (count));

    for (let row of meals) {
        var op = document.createElement("option");
        op.value = row.id;
        op.text = row.name;
        select.append(op);
    }
}


function changemeal_editmode(obj) {
    let id = obj.id;
    let check = $('#check_' + id);
    check.empty();
}


