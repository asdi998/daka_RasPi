<?php
// header('Access-Control-Allow-Origin: *');
// header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
// header('Access-Control-Allow-Methods: GET, POST, PUT,DELETE');

$picdir = 'faces/';
$pichost = 'https:/domain.com/daka/faces/';

if(isset($_GET['type'])){
    $page = $_GET['page'];
    $limit = $_GET['limit'];
    $limit = ' limit '.($page-1)*$limit.','.$limit;
    switch($_GET['type']){
        case 'user':
            $result = query_sql("select * from user".$limit);
            $users = array();
            foreach ($result as $user) {
                $users[] = array(
                    'id' => $user['id'],
                    'name' => $user['username'],
                    'url' => $user['url'],
                    'status' => $user['status'],
                    'statusmsg' => ($user['status'] == 'safety') ? '正常' : (($user['status'] == 'warning') ? '发热' : $user['status']),
                    'disabled' => $user['disabled'],
                    'disabledmsg' => ($user['disabled'] == 'false') ? '正常' : (($user['disabled'] == 'true') ? '禁用' : $user['disabled']),
                    'lasttime' => $user['lasttime'],
                    );
            }
            $count = query_sql('select count(id) from user')[0]['count(id)'];
            echo outputTable($users, $count);
            break;
        case 'log':
            $result = query_sql('select * from user');
            $usermap = array();
            foreach ($result as $user) {
                $usermap[$user['id']] = $user['username'];
            }
            $result = query_sql("select * from log order by id desc".$limit);
            $logs = array();
            foreach ($result as $log) {
                $logs[] = array(
                    'id' => $log['id'],
                    'uid' => $log['uid'],
                    'name' => $usermap[$log['uid']],
                    'temp' => $log['temp'],
                    'time' => $log['time'],
                    );
            }
            $count = query_sql('select count(id) from log')[0]['count(id)'];
            echo outputTable($logs, $count);
            break;
        case 'adduser':
            $username = $_GET['name'];
            query_sql('INSERT INTO user (username, disabled) VALUES ("'.$username.'", true)');
            echo '请求成功';
            break;
        case 'del':
            @unlink($picdir.$_GET['id'].".jpg");
            query_sql('DELETE from user where id='.$_GET['id']);
            echo '请求成功';
            break;
        case 'edit':
            $uid = $_POST['userid'];
            $username = $_POST['username'];
            $status = $_POST['status'];
            $lasttime = $_POST['lasttime'];
            $disabled = $_POST['disabled'];
            if($_FILES['file']){
                move_uploaded_file($_FILES["file"]["tmp_name"], $picdir.$uid.".jpg");
                $url = $pichost.$uid.".jpg";
                query_sql('UPDATE user set username="'.$username.'", url="'.$url.'", status="'.$status.'", lasttime="'.$lasttime.'", disabled="'.$disabled.'" where id='.$uid);
            }else{
                query_sql('UPDATE user set username="'.$username.'", status="'.$status.'", lasttime="'.$lasttime.'", disabled="'.$disabled.'" where id='.$uid);
            }
            echo '请求成功';
            break;
        case 'md5':
            $result = array();
            $list = scandir($picdir);
            foreach ($list as $file) {
                if (in_array($file, array('.', '..'))) {
                    continue;
                }
                $filename = $picdir.$file;
                $result[$file] = md5_file($filename);
            }
            echo json_encode($result);
            break;
    }
}

function outputTable($data=[], $count='10', $msg='', $code='0'){
    $output = array('code'=>$code, 'msg'=>$msg, 'count'=>$count, 'data'=>$data);
    return json_encode($output);
}

function query_sql($query) {
    $dbMs = 'mysql';
    //数据库类型
    $dbHost = '1.1.1.1';
    //数据库主机名
    $dbName = 'daka';
    //数据库名称
    $dbUser = 'daka';
    //数据库用户名
    $dbPass = '123456';
    //数据库用户密码
    $dsn = "$dbMs:host=$dbHost;dbname=$dbName";
    try {
        $dbh = new PDO($dsn,$dbUser,$dbPass);
        //初始化一个PDO对象，就是创建了数据库连接对象$dbh
        $row = $dbh->query($query);
        if (is_object($row)) {
            $row->setFetchMode(PDO::FETCH_ASSOC);
            //设置关联数组模式
            $rows = $row->fetchAll();
        } else {
            $rows = $row;
        }
        $dbh = null;
        //释放数据库连接
        return $rows;
    } catch (PDOException$e) {
        $dberror = "Error: ".$e->getMessage();
        //获取异常信息
        return $dberror;
        //返回异常
    }
}