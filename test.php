<?php
//username and password, account number and browser info
$username = 'test';
$password = 'test';
$acc = '1234567890';
$url = 'https://ib.bri.co.id/ib-bri/Login.html/en';
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$cookie = "/cookie/cookiebri.txt";
// create a new cURL resource
if(isset($_GET['captcha']) && $_GET['captcha']=='yes'){
  $j_token = $_POST['csrf_token_newib'];
  $j_captcha = $_POST['captcha_text'];

  $postdata1 = "csrf_token_newib=".urlencode($j_token)."&j_password=" . urlencode($password) . "&j_username=" . urlencode($username) . "&j_plain_username=" . urlencode($username) . "&j_plain_password=" . urlencode("") . "&j_code=" . urlencode($j_captcha) . "&j_language=" . urlencode("en_EN"). "&preventAutoPass=";

  $ch = curl_init();
  curl_setopt ($ch, CURLOPT_URL,"https://ib.bri.co.id/ib-bri/Homepage.html");
  curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
  curl_setopt ($ch, CURLOPT_USERAGENT, $user_agent);
  curl_setopt ($ch, CURLOPT_TIMEOUT, 20);
  curl_setopt ($ch, CURLOPT_FOLLOWLOCATION,1);
  curl_setopt ($ch, CURLOPT_AUTOREFERER,1);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
  curl_setopt($ch, CURLOPT_HEADER, FALSE);

  curl_setopt($ch, CURLOPT_POST, TRUE);
echo '<pre>';print_r("{
  \"csrf_token_newib\": $j_token,
  \"j_password\": $password,
  \"j_username\": $username,
  \"j_plain_username\": $username,
  \"j_plain_password\": \"\",
  \"j_code\": $j_captcha,
  \"j_language\": \"en_EN\",
  \"preventAutoPass\": \"\"
}");
  curl_setopt($ch, CURLOPT_POSTFIELDS, "{
    \"csrf_token_newib\": $j_token,
    \"j_password\": $password,
    \"j_username\": $username,
    \"j_plain_username\": $username,
    \"j_plain_password\": \"\",
    \"j_code\": $j_captcha,
    \"j_language\": \"en_EN\",
    \"preventAutoPass\": \"\"
  }");

  curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    "Host: ib.bri.co.id",
    "Origin: https://ib.bri.co.id",
    "Referer: https://ib.bri.co.id/ib-bri/Login.html/en"
  ));

  curl_setopt ($ch, CURLOPT_COOKIEJAR, getcwd() . $cookie);
  curl_setopt ($ch, CURLOPT_COOKIEFILE, getcwd() . $cookie);

  $content = curl_exec( $ch );
  $err     = curl_errno( $ch );
  $errmsg  = curl_error( $ch );
  $header  = curl_getinfo( $ch );
  echo $content;

}else{
  $ch = curl_init();
  // Curl to get data login page from BRI
  curl_setopt($ch, CURLOPT_HEADER, false);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
  curl_setopt($ch, CURLOPT_ENCODING,  'gzip');

  curl_setopt($ch, CURLOPT_USERAGENT, $user_agent);
  curl_setopt($ch, CURLOPT_CONNECTTIMEOUT ,60);
  curl_setopt($ch, CURLOPT_TIMEOUT, 60);
  curl_setopt($ch, CURLOPT_FAILONERROR, true);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_COOKIESESSION, true);
  //curl_setopt($ch, CURLOPT_HEADER, 0);
  curl_setopt($ch, CURLOPT_COOKIEFILE, getcwd() . $cookie);
  curl_setopt($ch, CURLOPT_COOKIEJAR, getcwd() . $cookie);
  curl_setopt($ch, CURLOPT_URL, $url);
  // grab URL and pass it to the browser
  $content = curl_exec( $ch );
  $err     = curl_errno( $ch );
  $errmsg  = curl_error( $ch );
  $header  = curl_getinfo( $ch );

  $header['errno']   = $err;
  $header['errmsg']  = $errmsg;
  $header['content'] = $content;
  $exp = explode("name=\"csrf_token_newib\" value=\"",$content);
	echo $csrf_token = substr($exp[1],0,32);
  echo $content;
  //echo '<img src="'.$contentCaptcha.'" />';
  echo '<form name="cpatcha" method="POST" action="http://localhost/bri/test.php?captcha=yes"><input name="captcha_text" type="text" /><input name="csrf_token_newib" value="'.$csrf_token.'" type="hidden" /><input type="submit" /></form>';

}
