$(function() {

  var game_start = false;

  $('body').keyup(function(event) {
    if (event.key === " " && game_start === false) {
      game_start = true;
      start();
    }
    if (event.key === "Escape") {
      location.reload();
    }
  })

  const start = () => {
    var cnt = 3;
    $('.start').text(cnt);
    const cnDown = setInterval(function(){
              cnt--;
              if (cnt > 0) {
                $('.start').text(cnt);
              } else {
                clearInterval(cnDown);
                game();
              }
        },1000);
  }

  async function game() {
    var miss = 0;
    var count_correct = 0;
    const length = Object.keys(proverbs).length;
    const starttime = performance.now();
    for (var i = 1; i <= length; i++) {
    var roma = proverbs[i][2];
      $('.container').html(`
        <div class="main h3">${proverbs[i][0]}</div>
        <div class="kana">${proverbs[i][1]}</div>
        <div class="roma">${roma}</div>
        <div class="output"><br></div>
        <div class="index">${i}/${length}</div>
        <div class="restart"><br><a href="">やり直す</a></div>`);
      var output = "";
      var n = 0;
      count_correct += roma.length;
      while (n < roma.length) {
        var ans = roma[n];
        if (roma[n] === '、') {
          ans = ',';
        }
        [n, output, miss] = await typing(n, ans, output, miss);
        if (output) {
        $(' .output').text(output);
        }
      }
    }
    const endtime = performance.now();
    const game_time = Math.round((endtime - starttime) / 10) / 100;
    display_result(count_correct, miss, game_time);
  }

  const typing = (n, str, output, miss) => {
    return new Promise(resolve => {
      $('body').keydown(function(event) {
        $('body').off('keydown');
        if (event.key === str.toLowerCase()) {
          output += str;
          n++;
          resolve([n, output, miss]);
        } else if (event.key === "Escape"){
          ;
        } else {
          $('body').css('background-color', 'rgb(255, 195, 195)');
          setTimeout(function() {
            $('body').css('background-color', 'white');
          }, 100);
          miss++;
          resolve([n, output, miss]);
        }
      })
    })

  }

  const display_result = (count_correct, miss, game_time) => {
    const count_total = count_correct + miss;
    const rate = count_correct / count_total;
    const percentage = Math.round(rate * 10000) / 100;
    const wpm = count_total * 60 / game_time;
    const score = Math.round(wpm * Math.pow(rate, 3));
    $('.container').html(`
      <div class="result">
        <h3>結果</h3>
        <div class="score">e-typingスコア:<span>${score}</span></div>
        <div class="time">タイム:<span>${game_time}秒</span></div>
        <div class="count">入力文字数:<span>${count_total}字</span></div>
        <div class="wpm">1分間当たり:<span>${Math.round(wpm)}字</span></div>
        <div class="miss">ミス:<span>${miss}回</span></div>
        <div class="percent">正確率:<span>${percentage}%</span></div>
        <div class="restart text-center"><br><a href="">やり直す</a></div>
      </div>
      `)
  }

})
