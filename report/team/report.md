# Báo cáo cá nhân — Research Agent Tool Eval

> Bài làm được thực hiện cá nhân để tự học; không có thành viên khác. Thông tin tên/MSSV không có trong workspace nên không tự điền.

## 1. Giới thiệu agent — Phần A

### Agent làm được gì?

Research Agent hỗ trợ tìm bài đăng trên mạng xã hội, tìm tin trên web, đọc URL và bài báo arXiv, tra cứu chính sách nội bộ, rồi định dạng kết quả thành digest. Agent hỏi lại khi thiếu thông tin; với thao tác gửi Telegram, chỉ gửi sau khi người dùng xác nhận nội dung cuối cùng. Tool calculator hỗ trợ tính bốn phép toán cơ bản tại chỗ, không gọi API ngoài.

### Chạy UI và link dùng thử

Chạy từ thư mục `starter_v0/`:

```bash
streamlit run app.py
```

UI được cấu hình dùng OpenRouter; cần khai báo `OPENROUTER_API_KEY` trong `starter_v0/.env`. Địa chỉ local mặc định sau khi khởi chạy: [http://localhost:8501](http://localhost:8501). Chưa có bằng chứng deploy public trong workspace, nên đây không phải link truy cập từ máy khác.

### Các tool

| Tool | Chức năng |
|---|---|
| `clarify` | Hỏi người dùng khi thiếu thông tin hoặc cần xác nhận. |
| `timeline` | Lấy bài đăng gần đây từ một tài khoản cụ thể. |
| `social_search` | Tìm bài đăng theo chủ đề hoặc từ khóa. |
| `lookup` | Tìm thông tin chung hoặc tin tức trên web. |
| `fetch` | Đọc nội dung từ URL cụ thể. |
| `format` | Định dạng các kết quả đã thu thập thành digest. |
| `send` | Gửi nội dung lên Telegram sau khi được xác nhận. |
| `policy` | Tra cứu tài liệu chính sách nội bộ. |
| `papers` | Tìm bài báo khoa học trên arXiv. |
| `paper_text` | Lấy nội dung bài báo từ kết quả tìm kiếm arXiv. |
| `calculator` | Thực hiện cộng, trừ, nhân, chia hai số; chạy local, không gọi API ngoài. |

Khai báo tool: [`tools.yaml`](../../starter_v0/artifacts/tools.yaml). Tool mới: [`calculator/tool.py`](../../starter_v0/tools/calculator/tool.py) và [`calculator/TOOL.md`](../../starter_v0/tools/calculator/TOOL.md).

### Câu hỏi mẫu

1. “Tweet mới nhất của Sam Altman là gì?”
2. “Tin tức AI hôm nay có gì nổi bật?”
3. “Tóm tắt bài này giúp mình: https://openai.com/blog/gpt-5”
4. “Tìm bài báo arXiv về AI agent evaluation.”
5. “Tính 10 cộng 20.”

## 2. Giải pháp

- Tinh chỉnh [`system_prompt.md`](../../starter_v0/artifacts/system_prompt.md) và [`tools.yaml`](../../starter_v0/artifacts/tools.yaml) để định tuyến tool, hỏi khi thiếu dữ liệu và phân biệt xin nội dung với xác nhận gửi.
- Sửa case R12 trong `eval_base.json` để đưa sẵn nội dung cuối cùng cần xác nhận; như vậy `yes_no` được kiểm tra trong đúng bối cảnh.
- Thêm calculator độc lập, đăng ký trong `tools/__init__.py`, khai báo schema và hỗ trợ `a`, `b`, `operation` (`add`, `subtract`, `multiply`, `divide`).
- Xây dựng 10 case calculator trong [`eval_group.json`](../../starter_v0/data/eval_group.json): 5 single-turn và 5 multi-turn.

## 3. Kết quả và bằng chứng — Phần B

### B1. Kết quả v0–v3

Chỉ số dưới đây lấy từ `summary.case_accuracy` trong run JSON. Cả bốn run đều có `measured_cases == total_cases` và `provider_error_cases == 0`. v0 là baseline; các mục thay đổi/giả thuyết v1–v3 theo [`version_log.csv`](../../starter_v0/artifacts/version_log.csv).

| Version | Thay đổi chính | Giả thuyết | Accuracy | Run |
|---|---|---|---:|---|
| v0 | Baseline | Đo hành vi ban đầu | 0.65 (13/20) | [v0 JSON](../../starter_v0/runs/v0_B_base_openrouter_20261110T232727572862.json) |
| v1 | `system_prompt.md` và khai báo tools | Làm rõ định tuyến và cách truyền tham số | 0.95 (19/20) | [v1 JSON](../../starter_v0/runs/v1_B_base_openrouter_20261111T100952031377.json) |
| v2 | Làm rõ quy tắc `clarify` trong `tools.yaml` | Phân biệt hỏi nội dung còn thiếu với xác nhận nội dung đã hoàn chỉnh | 0.95 (19/20) | [v2 JSON](../../starter_v0/runs/v2_B_base_openrouter_20261111T102815623143.json) |
| v3 | Làm rõ ranh giới xác nhận trong prompt và sửa case R12 | Kiểm tra xác nhận khi đã có nội dung cụ thể | 1.00 (20/20) | [v3 JSON](../../starter_v0/runs/v3_B_base_openrouter_20261111T105533956231.json) |

Cả bốn run dùng OpenRouter với `openai/gpt-4o-mini`. v3 đạt tool-routing, argument và multiturn accuracy đều 1.0 trong base suite.

### B2. Phân tích lỗi

| Run/case | Bằng chứng lỗi | Phân tích và xử lý |
|---|---|---|
| v0 / R03 | `lookup` nhận `query="AI news"` thay vì `"AI"` | Tham số truy vấn không khớp kỳ vọng; làm rõ quy ước truy vấn trong khai báo tool. |
| v0 / R08, R14 | Gọi `send` cho yêu cầu ngoài phạm vi thay vì không gọi tool | Thiếu ranh giới phạm vi đủ rõ; system prompt v1 nêu rõ chỉ trả lời trong phạm vi research agent. |
| v0 / R10, R11 | Đoán tài khoản hoặc URL thay vì gọi `clarify` | Bổ sung nguyên tắc không đoán username/URL và hỏi khi thiếu thông tin. |
| v0 / R12 | Gọi `send` mà chưa hỏi xác nhận | Bổ sung ranh giới xác nhận; v1/v2 còn chọn `text` vì case chưa cung cấp nội dung. |
| v0 / R13 | `lookup` dùng query `"AI news"` và thiếu `topic="news"` | Làm rõ phân biệt tìm tin tức và từ khóa truy vấn. |
| v1–v2 / R12 | Gọi `clarify` nhưng dùng `response_type="text"` thay vì `yes_no` theo expected | Case cũ không có nội dung cụ thể nên kỳ vọng chưa khớp hành vi hợp lý. Sửa case để cung cấp nội dung, đồng thời làm rõ prompt; R12 pass ở v3. |

Các lỗi trên lấy từ `results[*].result.failures` trong run JSON tương ứng; v3 base không còn failure.

### B3. Evaluation do cá nhân bổ sung

Run group có 10/10 case pass, `case_accuracy=1.0`, không có provider error. Kết quả chi tiết: [v3 group JSON](../../starter_v0/runs/v3_B_group_openrouter_20261111T114310251754.json).

| Case | Kiểu | Điều kiểm tra | Kết quả |
|---|---|---|---|
| G01 calculator add | Single | Cộng 10 và 20 | Pass |
| G02 calculator subtract | Single | Trừ đúng thứ tự 9 − 4 | Pass |
| G03 calculator multiply | Single | Ánh xạ “tích” sang multiply | Pass |
| G04 calculator divide | Single | Chia đúng thứ tự 81 / 9 | Pass |
| G05 calculator decimal add | Single | Cộng hai số thập phân | Pass |
| G06 calculator multiturn divide | Multi | Giữ hai số lượt trước, dùng phép chia ở lượt sau | Pass |
| G07 calculator multiturn add | Multi | Tham chiếu “hai số đó” từ lượt trước | Pass |
| G08 calculator multiturn correct operand | Multi | Giữ phép nhân, cập nhật toán hạng thứ hai | Pass |
| G09 calculator multiturn subtract | Multi | Giữ toán hạng và thứ tự phép trừ qua nhiều lượt | Pass |
| G10 calculator multiturn new request | Multi | Ưu tiên phép tính mới thay cho yêu cầu cũ | Pass |

### B4. Transcript chat

Workspace hiện chỉ có [`example_openrouter_20260101T030000000000.transcript.json`](../../starter_v0/samples/transcripts/example_openrouter_20260101T030000000000.transcript.json). Đây là transcript mẫu với kết quả `[MOCK]`, không phải bằng chứng live chat thật. Mẫu minh họa ba lượt:

| Lượt | Yêu cầu | Tool minh họa | Kết quả trong mẫu |
|---|---|---|---|
| 1 | Tin AI hôm nay có gì nổi bật? | `lookup` | Trả digest từ mock results |
| 2 | Tóm tắt vài tweet mới nhất | `clarify` | Hỏi tài khoản nào |
| 3 | Của Andrej Karpathy, lấy 5 bài | `timeline` | Gọi với `screenname=karpathy`, `limit=5` |

Chưa tìm thấy transcript live thực tế trong `starter_v0/transcripts/`; phần này cần bổ sung nếu có chạy `chat.py` và lưu transcript.

### B5. Tool mới, unit test và UI

| Hạng mục | Bằng chứng | Kết quả / giới hạn |
|---|---|---|
| Tool mới | [`calculator/tool.py`](../../starter_v0/tools/calculator/tool.py), [`calculator/TOOL.md`](../../starter_v0/tools/calculator/TOOL.md), [`tools.yaml`](../../starter_v0/artifacts/tools.yaml), [`tools/__init__.py`](../../starter_v0/tools/__init__.py) | Tính bốn phép toán local; không cần API ngoài. |
| Unit test calculator | [`test_tools_calculator.py`](../../starter_v0/tests/test_tools_calculator.py) | 6 test case pass: bốn phép toán, chia cho 0, operation không hỗ trợ. Unit test bắt lỗi chia cho 0 và operation không hợp lệ; group eval hiện chỉ đánh giá tool call/arguments nên không thay thế kiểm tra kết quả thực thi và đường lỗi này. |
| Toàn bộ unit test | Lệnh `pytest tests/ -q` | **73 passed, 17 skipped**, 0 failed. 17 test bị skip là các stub TODO trong `test_tools_todo.py`; vì vậy chưa đạt điều kiện toàn suite 0 skipped. |
| UI | [`app.py`](../../starter_v0/app.py), [`requirements.txt`](../../starter_v0/requirements.txt) | Có ứng dụng Streamlit; lệnh chạy và URL local ở Phần A. Chưa có URL public/deploy được xác minh. |

### B6. Bonus evidence

Chưa có bằng chứng chạy model local, gửi thật lên Telegram sau xác nhận, hoặc toàn suite 0 skipped. `send`, `policy`, `papers`, `paper_text` là tool có sẵn của bài lab, không tính là tool mới tự viết.

### B7. Small Local Model Challenge

Không có run Ollama/model local trong `starter_v0/runs/`; không báo cáo metric cho hạng mục này.

## 4. Khó khăn và cách xử lý

- **Định tuyến và tham số chưa chính xác ở baseline:** v0 đạt 13/20. Đọc failure cụ thể trong run JSON, sau đó sửa prompt/tool declarations theo từng vấn đề; v1 đạt 19/20.
- **Kỳ vọng xác nhận ở R12 chưa đúng bối cảnh:** câu hỏi ban đầu không đưa nội dung bản tin nhưng lại kỳ vọng `yes_no`. Sửa case để có nội dung cuối cùng cụ thể và bổ sung quy tắc phân biệt `text`/`yes_no`; v3 base pass 20/20.
- **Chữ ký calculator không khớp cách gọi mong muốn:** ban đầu nhận `expression`, nhưng yêu cầu kiểm tra truyền `a`, `b`, `operation` gây `TypeError`. Đổi giao diện/schema sang ba tham số, thêm test regression và 10 eval case calculator.
- **Bằng chứng triển khai còn thiếu:** hiện không có transcript live hoặc public UI URL trong workspace; báo cáo chỉ dẫn transcript mẫu và URL local, không trình bày chúng như kết quả live/deploy.
- **Còn test stub chưa triển khai:** 17 test TODO đang skip. Calculator có test riêng và toàn suite không có failure, nhưng cần hoàn thiện các test stub nếu muốn đạt 0 skipped.

## 5. Hạn chế và hướng cải thiện

- Base suite và group suite đều đạt 100% trong các run hiện có, nhưng mỗi suite chỉ có 20 và 10 case; kết quả không chứng minh độ bao phủ mọi cách diễn đạt hoặc mọi tình huống thực tế.
- Group eval đo routing và arguments, chưa đo kết quả tính toán đầu ra; unit test calculator hiện đảm nhiệm kiểm tra phép tính và một số trường hợp lỗi.
- Hoàn thiện các test TODO còn skip; chạy lại suite và lưu output làm bằng chứng.
- Chạy ít nhất ba lượt chat thật bằng `chat.py`, lưu transcript; nếu cần chia sẻ cho người khác, deploy UI và cập nhật public URL.
- Bổ sung thêm case biên cho calculator, ví dụ số âm, số thập phân, thiếu tham số và số chia bằng 0 ở tầng thực thi tool.

## 6. Tài liệu tham khảo

- [README dự án](../../README.md)
- [Hướng dẫn starter](../../starter_v0/README.md)
- [Hướng dẫn cấu hình tool/API](../../docs/TOOL-SETUP.md)
- [Version log](../../starter_v0/artifacts/version_log.csv)
