# error_message 是前端需要展示出来的错误信息

# 成功
CLACK_SUCCESS = {"error_code": 0, "error_message": "OK"}

# 未知错误
CLACK_UNEXPECTED_ERROR = {"error_code": -1, "error_message": "未知错误"}

# 请求方法不是POST
CLACK_POST_REQUIRED = {"error_code": 1, "error_message": "请求方法不是POST,触发该错误应该是前端写挂了"}

# 请求JSON中部分必须的对象不存在
CLACK_REQUEST_JSON_ERROR = {"error_code": 2, "error_message": "请求JSON中部分必须的对象不存在,触发该错误应该是前端写挂了"}

# 传递的值为空
CLACK_NULL_ERROR = {"error_code": 3, "error_message": "存在空值"}

# 目标不存在
CLACK_NOT_EXISTS={"error_code": 4, "error_message": "此目标不存在"}

# 名称已经存在
CLACK_NAME_EXISTS = {"error_code": 5, "error_message": "已存在"}

# 有重复的内容
CLACK_REPEAT_CONTENT = {"error_code": 6, "error_message": "有重复"}
#
# # 登录错误
# CLACK_USER_LOGIN_FAILED = {"error_code": 4, "error_message": "登录失败,用户名或密码错误"}
#
# # 用户未登录
# CLACK_LOGIN_REQUIRED = {"error_code": 5, "error_message": "请先登录"}
#
# # 需要系统管理员权限
# CLACK_ADMIN_REQUIRED = {"error_code": 6, "error_message": "只有系统管理员才能进行此操作"}
#
# # 创建Model失败
# CLACK_CREATE_NEW_MODELS_FAILED = {"error_code": 7, "error_message": "创建失败"}
#
# # 接口还未实现
# CLACK_UNIMPLEMENTED_API = {"error_code": 8, "error_message": "API接口尚未实现"}
#
# # 没有权限
# CLACK_NO_PERMISSION = {"error_code": 9, "error_message": "没有调用这个接口的权限"}
#
# # student不存在
# CLACK_STUDENT_NOT_EXISTS = {"error_code": 10, "error_message": "查询的学生不存在"}
#
# # student不存在
# CLACK_TEACHER_NOT_EXISTS = {"error_code": 11, "error_message": "查询的教师不存在"}
#
# # course不存在
# CLACK_COURSE_NOT_EXISTS = {"error_code": 12, "error_message": "查询的课程不存在"}
#
# # 学生的成绩score不存在
# CLACK_SCORE_NOT_EXISTS = {"error_code": 13, "error_message": "这名学生的成绩不存在或者数据库中存在两门同样的成绩"}
#
# # 老师没有教过这名学生
# CLACK_TEACH_NOT_EXISTS = {"error_code": 14, "error_message": "这名老师没有教过这名学生课"}
#
# # 班级不存在
# CLACK_BANJI_NOT_EXISTS = {"error_code": 15, "error_message": "查询的班级不存在"}
#
# #选课记录不存在
# CLACK_SELECTION_NOT_EXISTS = {"error_code": 16, "error_message": "查询的选课记录不存在"}
#
# #教室不存在
# CLACK_CLASSROOM_NOT_EXISTS = {"error_code": 17, "error_message": "查询的教室不存在"}
#
# #学院不存在
# CLACK_DEPARTMENT_NOT_EXISTS = {"error_code": 18, "error_message": "查询的学院不存在"}
#
# #保存失败
# CLACK_SAVE_FAIL = {"error_code": 19, "error_message": "保存失败"}
#
# #删除失败
# CLACK_DELETE_FAIL = {"error_code": 20, "error_message": "删除失败"}
#
# #选课失败
# CLACK_SELECTION_FAIL = {"error_code": 21, "error_message": "选课失败"}
#
# #学生查询课表失败
# CLACK_TIMETABLE_FAIL={"error_code": 22, "error_message": "查询课表失败"}
#
# #DateAndClassroom查询失败
# CLACK_DATEANDCLASSROOM_NOT_EXISTS = {"error_code": 23, "error_message": "查询日期和班级失败"}
#
# #下载失败
# CLACK_DOWNLOAD_FAILED = {"error_code": 24, "error_message": "下载失败"}
#
# #课程余量修改失败
# CLACK_ALLOWANCE_UPDATE_FAILED={"error_code": 25, "error_message": "课程余量修改失败"}
#
# #设置学年学期失败
# CLACK_SET_YEAR_SEMESTER_FAIL={"error_code": 26, "error_message": "设置学年学期失败"}
#
# #查询学年学期失败
# CLACK_INQUIRY_YEAR_SEMESTER_FAIL={"error_code": 27, "error_message": "查询学年学期失败"}
#
# #获取报表失败
# CLACK_REPORT_FAIL={"error_code": 28, "error_message": "获取报表失败"}
#
# #目标不存在
# CLACK_NOT_EXISTS={"error_code": 29, "error_message": "此目标不存在"}
#
# #学生选题限选一个且已经选择课题
# CLACK_STUDENT_SELECT_DST_EXISTS={"error_code": 30, "error_message": "已经选择课题"}
#
# #上传文件失败
# CLACK_DISSERTATION_UPLOAD_FILE_FAILED={"error_code": 31, "error_message": "上传论文失败"}
#
# # 密码错误
# ClACK_ERROR_PASSWORD = {"error_code": 32, "error_message": "密码错误"}