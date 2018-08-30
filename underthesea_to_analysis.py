from underthesea import ner, word_tokenize
from collections import Counter


def create_counter_tokenize(content):
    return Counter(word_tokenize(content))


def test_time(content):
    result = word_tokenize(content)
    print(result)

# if __name__ == '__main__':
#     content = 'Thế nhưng rắc rối chưa dừng lại khi U23 Iraq tuyên bố bỏ cuộc vì đội trẻ liên quan đến gian lận tuổi. Ban tổ chức một lần nữa phải điều chỉnh kết quả bốc thăm khi chuyển U23 UAE về bảng C, thế chỗ U23 Iraq. Không những vậy, việc có 6 bảng đấu, bảng A lại có 5 đội thay vì 4 như 5 bảng còn lại và lấy đến 16 đội vào vòng 1/8 cũng tạo ra không ít rắc rối và tranh cãi.Vì thể thức lấy 2 đội dẫn đầu 6 bảng cùng 4 đội xếp thứ 3 có thành tích xuất sắc nhất nên lượt cuối cùng vòng bảng rất phức tạp và cũng tạo ra nhiều luồng tranh luận khi xếp cặp đấu cho các đội đứng thứ 3 giành vé đi tiếp.Với khá nhiều thể thức lạ như vậy, người hâm mộ đang đặt không ít dấu hỏi trước vòng 1/8, vòng loại trực tiếp đầu tiên. Ở vòng đấu này có nhiều cặp đấu cân tài cân sức và hứa hẹn không thể giải quyết thắng thua ngay trong 90 phút chính thức. Vậy câu hỏi đặt ra là ban tổ chức sẽ dùng phương án nào để phân định vé vào tứ kết?U23 Việt Nam sẽ chạm trán U23 Bahrain, đây là đối thủ nhiều duyên nợ nên thầy trò HLV Park Hang Seo không dám chắc khả năng giải quyết trong 2 hiệp chính thức. Những buổi tập gần đây, chiến lược gia người Hàn Quốc đã tính đến phương án đá luân lưu nên cho các học trò tích cực tập luyện.'
#     test_time(content)
