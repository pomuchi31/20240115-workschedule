let calendar;
let selectedDate = null;

window.addEventListener("load", () => {

  // カレンダーの移動関係のボタンを取得する。
  const today = document.querySelector(".fc-today-button");
  const next  = document.querySelector(".fc-next-button");
  const prev  = document.querySelector(".fc-prev-button");

  // start と end の入力欄に表示しているカレンダーの日付を与える
  const definition = () => {

      // Dateオブジェクトを適したフォーマットに変更
      const format_date   = (date) => {
          const year  = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day   = String(date.getDate()).padStart(2, '0');

          return `${year}-${month}-${day}`;
      }

      // タイトルから年月を取り出す。2024年1月 → [ "2024年1月", "2024", "1" ]
      const title         = document.querySelector(".fc-toolbar-title").textContent;
      const pattern       = /(\d{4})年(\d{1,2})月/;
      const result        = title.match(pattern);

      if (result){
          console.log(result);

          const year  = Number(result[1]);
          const month = Number(result[2]);

          // startの年月日を取得する。Dateクラスはmonthが0からスタートする。0と指定すると1月になる。
          const start         = new Date( year , month-1 , 1);

          //来月のDateオブジェクトを作り、1日引く。今月の最終日を作る。
          const next_month    = new Date( year , month , 1)
          const end           = new Date( next_month - 1 );

          // 適切なフォーマットに変換した文字列の日付を、hiddenフォームに与える。
          console.log("definition_start element:", document.querySelector("#definition_start"));
          console.log("definition_end element:", document.querySelector("#definition_end"));
          

          document.querySelector("#definition_start").value   = format_date(start);
          document.querySelector("#definition_end").value     = format_date(end);
          
      }

  }

  today.addEventListener("click", definition );
  next.addEventListener( "click", definition );
  prev.addEventListener( "click", definition );


  // カレンダー移動しなくても、ロード時に入力欄にセットしておく。
  definition();


});

document.addEventListener('DOMContentLoaded', () => {
  const calendarEl = document.getElementById('calendar');
  calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'local',
    timeZone: 'local',
    eventDisplay: 'block',
    displayEventTime: false,
    selectable: true,
    // views.py schedule_data より、JSONを受け取っている。
    //これにより、カレンダーに表示しているデータだけ収得できる。）
    events: {
      url: '/workschedule/schedule_data/'     
    },
    select: arg => {
      selectedDate = arg.startStr;  // クリックした日付を変数に保存
      console.log("Calendar selected", arg);
      initEditModal(arg);
    },
    eventClick: arg => {
      console.log("Event clicked", arg);
      initEditModal(arg);
    },
  });

  calendar.render();

  const initEditModal = data => {

    console.log("=====");
    console.log(data);

    console.log("=====");


    removeAlreadyModal();
    const defModal = document.getElementById('exampleModal');
    defModal.classList.add('modal-centered');
    const bootstrapModal = new bootstrap.Modal(defModal);
    bootstrapModal.show();
    document.body.appendChild(defModal);


    if (data.event === undefined) {
      const deleteElem = document.querySelector('#defModal .delete');
      if (deleteElem) {
        deleteElem.remove();
      }
    
    //デフォルト(新規作成）のフォームを表示させる。

    document.querySelector("[name='item1']").value = USER_INFO.item1;
    document.querySelector("[name='item2']").value = USER_INFO.item2;
    document.querySelector("[name='item3']").value = USER_INFO.item3;
    document.querySelector("[name='item4']").value = USER_INFO.item4;
    document.querySelector("[name='item5']").value = USER_INFO.item5;
    document.querySelector("[name='item6']").value = USER_INFO.item6;
    document.querySelector("[name='item7']").value = USER_INFO.item7;
    document.querySelector("[name='item8']").value = USER_INFO.item8;

    //編集対象は未指定に
    document.querySelector("[name='id']").value = "";

  }//ここに書き加え
    else{
    
    // 編集時のフォームを表示させる。
    console.log("編集時のフォーム変更");
    console.log(data.event.extendedProps.item1);
    console.log(data.event.extendedProps.item2);
    console.log(data.event.extendedProps.item3);
    console.log(data.event.extendedProps.item4);
    console.log(data.event.extendedProps.item5);
    console.log(data.event.extendedProps.item6);
    console.log(data.event.extendedProps.item7);
    console.log(data.event.extendedProps.item8);

    document.querySelector("[name='item1']").value = data.event.extendedProps.item1;
    document.querySelector("[name='item2']").value = data.event.extendedProps.item2;
    document.querySelector("[name='item3']").value = data.event.extendedProps.item3;
    document.querySelector("[name='item4']").value = data.event.extendedProps.item4;
    document.querySelector("[name='item5']").value = data.event.extendedProps.item5;
    document.querySelector("[name='item6']").value = data.event.extendedProps.item6;
    document.querySelector("[name='item7']").value = data.event.extendedProps.item7;
    document.querySelector("[name='item8']").value = data.event.extendedProps.item8;
    //編集対象のidをフォームにセットする。
    document.querySelector("[name='id']").value = data.event.id;
  }
    setupModalData(defModal, data);
    registerEditModalEvent(defModal, data);
  }

  const setupModalPosition = (modal, e) => {
    const position = calcModalPosition(e);
    modal.style.left = `${position.x}px`;
    modal.style.top = `${position.y}px`;
  };

  const calcModalPosition = e => {
    const windowWidth = window.outerWidth;

    const y = e.pageY + 16;
    let x = e.pageX;

    if (e.pageX <= 125) {
      x = e.pageX;
    } else if (e.pageX > 125 && windowWidth - e.pageX > 125) {
      x = e.pageX - 125;
    } else if (windowWidth - e.pageX <= 125) {
      x = e.pageX - 250;
    }

    return {
      x: x,
      y: y
    };
  };

  const removeAlreadyModal = () => {
    const modal = document.getElementById('modal');
    if (modal) {
      modal.remove();
    }
  };

  // モーダル登録処理
  const registerEditModalEvent = (modal, arg) => {

    // 保存
    const saveButton = modal.querySelector('#save');
    if (saveButton) {
      saveButton.addEventListener('click', e => {
        e.preventDefault();
        console.log('Save button clicked');

        const start = modal.querySelector('#start').value;
        const end = modal.querySelector('#end').value;
        const title = modal.querySelector('#title').value;
        const color = modal.querySelector('#color').value;

        const data = {
          start: start,
          end: end,
          title: title,
          color: color
        };

        fetch('/surveyCalendar_view/', {
          method: 'POST',
          body: new FormData(document.querySelector('form')),
          headers: {
            'X-CSRFToken': csrfToken
          }
        }).then, response => {
          if (response.ok) {
            // 保存が成功した場合の処理
            const successMessage = document.getElementById('Save');
            const errorMessage = document.getElementById('Error');
            fetch('/surveyCalendar_view/', {
              method: 'POST',
              body: new FormData(),
              headers: {
                const: csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value,
              }
            })
              .then(response => {
                if (response.ok) {
                  // 保存が成功した場合の処理
                  successMessage.style.display = 'block';
                  // エラーメッセージを非表示にする
                  errorMessage.style.display = 'none';
                } else {
                  // エラーメッセージを表示する
                  errorMessage.textContent = '保存に失敗しました。';
                  errorMessage.style.display = 'block';
                  // 成功メッセージを非表示にする
                  successMessage.style.display = 'none';
                }

                calendar.unselect();
                modal.remove();
              });
          };

          // DateObject to YYYY-MM-DD
          function formatDate(date) {
            var d = new Date(date),
              month = '' + (d.getMonth() + 1),
              day = '' + d.getDate(),
              year = d.getFullYear();

            if (month.length < 2)
              month = '0' + month;
            if (day.length < 2)
              day = '0' + day;
            return [year, month, day].join('-');
          }
        }
      }
      )
    }
  }
})

const setupModalData = (modal, data) => {
  const start = modal.querySelector('#id_date');

  console.log(data);
  if (data.event !== undefined) {
    start.value = /T/.test(data.event.startStr) ? data.event.startStr.split('T')[0] : data.event.startStr;
  }
  else {
    start.value = data.startStr;
  }

};

