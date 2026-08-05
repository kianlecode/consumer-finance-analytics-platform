-- Hàm dùng chung cho các bảng có cột updated_at, dùng để tự động cập nhật cột updated_at khi có bản ghi được cập nhật
-- Tạo hàm tại từng database
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;