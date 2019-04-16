# classにしている
class CommonDirectResponseSaver

  # SSLサーバ証明書を使う？
  require "openssl"
  # 初期設定 通貨ペア、終了時間()、取得間隔を設定 
  def initialize(pair:, stop_time:, interval_time:)
    @pair = pair
    @stop_time = stop_time
    @interval_time = interval_time

    # public APIだから空で良い
    @headers = {
        "ACCESS-KEY" => "",
        "ACCESS-NONCE" => "",
        "ACCESS-SIGNATURE" => ""
    }
  end

  # !を付けると呼び出したオブジェクト自体が影響を受けるようになる
  def execute!
    id = 0
    # @~はこのクラスを継承する時に設定する,'w'は書き込みのコマンド
    CSV.open(@csv_file_path,'w') do |test|
      # %w は配列を作る演算子らしい、["id","json_body","trade_time_int","pair"]の配列をtest(csvファイル)に挿入
      test << %w(id json_body trade_time_int pair)
      # 終了時間になるまでループ
      while @stop_time > Time.zone.now # 時間が停止指定時間
        # ~年~月~日~時~分~秒にフォーマットした現在時刻
        now_time_int = Time.zone.now.strftime("%Y%m%d%H%M%S").to_i
        id += 1
        # begin-rescueで例外処理
        begin
          retries = 0
          # Zaifの場合
          # @https = Net::HTTP.new(@uri.host, @uri.port) 
          # @uri = URI.parse("https://api.zaif.jp/api/1/ticker/#{@pair}")
          # startメソッドでサイトに接続
          response = @https.start {
            @https.get(@uri.request_uri, @headers)
          }
        rescue => e
          retries += 1
          if retries < 3
            retry # <-- Jumps to begin
          else
            # Error handling code, e.g.
            puts "Couldn't connect to proxy: #{e}"
          end
        end
        # コード型がNet::HTTPOKだったらcsvファイルにid、レスポンスの内容、時刻、通貨ペアを記入
        test << if response.code_type == Net::HTTPOK
                  [id, response.body, now_time_int, @pair]
                else
                  [id, "取得失敗", now_time_int, @pair]
                end

        # 取得停止時間と現時刻の差(秒)
        diff_sec = @stop_time - Time.zone.now
        if diff_sec > @interval_time
          sleep @interval_time
        elsif diff_sec > 0
          sleep diff_sec
        end
      end
    end
  end
end