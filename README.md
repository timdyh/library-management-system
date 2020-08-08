### <a href="https://github.com/TimDyh/library-management-system" target="_blank">项目 GitHub 仓库</a>



## 项目需求

![requirements](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-19-060202.png)



## 系统建模

### 活动图

普通用户注册后通过前台页面登录，进行浏览、查询、借书、还书等操作。

图书馆管理员通过后台管理界面登录，可直接对数据库进行增删改查操作。

![活动图](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153948.jpg)

### 用例图

1. **首页**

   用户可以选择登录或注册。

   ![用例图-首页](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153949.jpg)

2. **个人中心**

   用户可以浏览借阅列表，对列表中的书籍进行还书操作。如果逾期，则还需要缴纳罚金。

   ![用例图-个人中心](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153950.jpg)

3. **借书页面**

   用户首先通过输入关键字查询相关书籍，然后对返回列表中的书籍进行借书操作。

   ![用例图-借书页面](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153951.jpg)

4. **后台管理**

   管理员登录后台后可以查看数据库和日志信息，必要时进行增删改查操作。

   ![用例图-后台管理](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153952.jpg)

### 类图

在 Django 框架下，所有数据库表模型均继承于 `Model` 类，所有视图逻辑均继承于 `View` 类。控制器与用户进行交互，并提供模型数据至视图，实现数据与逻辑的解耦。

![类图](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153953.jpg)

| 模型   | 描述                                                         |
| ------ | ------------------------------------------------------------ |
| User   | 用户表，保存所有的用户信息，包括用户名、姓名、密码（摘要）字段，与 Book 存在多对多关系。 |
| Book   | 书目表，保存所有的书籍信息，包括书号、书名、作者、出版社、是否可借字段。 |
| Borrow | 借阅关系表，保存所有的借阅信息，包括序号、借阅者、所借书籍、借出时间、归还期限字段，其中借阅者和所借书籍分别是参照 User 和 Book 的外键。 |
| Log    | 日志表，保存所有注册、登录、登出、借书、还书的记录，包括序号、时间、用户、相关书籍、操作字段，其中用户和相关书籍分别是参照 User 和 Book 的外键。 |

| 视图         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| RegisterView | 注册视图，获取新用户的信息进行注册。                         |
| LoginView    | 登录视图，获取用户名和密码进行登录，并将当前用户状态存入 Session。 |
| LogoutView   | 登出视图，清空 Session，登出。                               |
| HomeView     | 个人中心视图，显示用户的借阅列表，并提供还书按钮。           |
| SearchView   | 查询视图，通过输入关键字进行查询，返回相关的书籍列表，并提供借书按钮。 |
| BorrowView   | 借书视图，完成借书逻辑。                                     |
| ReturnView   | 还书视图，完成还书逻辑，若逾期则给出缴纳罚金提示。           |

### 顺序图

1. **注册**

   用户打开注册页面，输入个人信息，RegisterView 获得后向 User 查询该用户是否不存在，若是则在 User 中增添该用户，并将本次注册操作写入 Log，然后返回注册成功信息。

   ![顺序图-注册](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153954.jpg)

2. **登录**

   用户打开登录页面，输入用户名和密码，LoginView 获得后向 User 查询该用户是否存在，若是则将本次登录操作写入 Log，然后跳转页面到用户的个人中心。HomeView 向 Borrow 查询该用户的借阅信息，并返回借阅列表。

   ![顺序图-登录](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153955.jpg)

3. **借书**

   用户打开查询界面，输入想要借的书籍的关键字，SearchView 获得后向 Book 查询相关书籍，并返回书籍列表。用户点击列表项目的借书按钮，BorrowView 向 Borrow 中增添一条该用户的借书记录，然后在 Book 中将该书籍设置为不可借，并将本次借书操作写入 Log，最后返回借书成功信息。

   ![顺序图-借书](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-153958.jpg)

4. **还书**

   用户打开个人中心页面，HomeView 向 Borrow 查询该用户的借阅信息，并返回借阅列表。用户点击列表项目的还书按钮，ReturnView 从 Borrow 中删除这条借书记录，然后在 Book 中将该书籍设置为可借，并将本次还书操作写入 Log，最后返回还书成功信息。如果还书逾期，则还将返回缴纳罚金的提示信息。

   ![顺序图-还书](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-154006.jpg)

### 状态图

![状态图](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-154013.jpg)



## 系统部署说明

### Requirements

* Python 3.6

* Django 3
* Bootstrap 3
* jQuery 3
* MySQL 8

### 启动系统

1. 在 MySQL 中新建一个名为 `library` 的数据库，字符集选择 `UTF-8` 。

2. 安装 MySQL 驱动 `mysqlclient` 。

   ```
   pip install mysqlclient
   ```

3. 在 `library/library/settings.py` 中配置数据库的 `USER` 和 `PASSWORD`。

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'library',
           'USER': '****',
           'PASSWORD': '************',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

4. 进入项目目录下。

   ```bash
   cd ./library
   ```

5. 迁移数据库。

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 启动系统。

   ```bash
   python manage.py runserver
   ```

7. 访问 127.0.0.1:8000 。



## 展示后修改和优化说明

1. 增加注册时的合法性检验：学号必须为 8 位（多于 8 位的部分无法输入），密码不能少于 6 位，否则将给出提示。

   ![学号](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-154014.jpg)

   ![密码](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-154015.jpg)

2. 实现对书名、作者、出版社三个字段的模糊查询。此外，将有馆藏记录但当前已借出的书籍也显示出来（没有借书按钮），而不是仅展示当前能借的书籍。这样能告诉用户这本书是有的，只是当前已经被别人借走了，可以过一段时间再来查询。

   ![借书](https://ipichub.oss-cn-hangzhou.aliyuncs.com/2020-07-18-154024.jpg)
