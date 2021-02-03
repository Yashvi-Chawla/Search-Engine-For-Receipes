<!DOCTYPE html> 
<html> 
	<head> 
		<title>Result page</title> 
		
<style type="text/css">
.results {
	margin-left:12%; 
	margin-right:12%; 
	margin-top:10px;
	font-family :arial,sans-serif;
	width:632px;
	margin-bottom: 26px;
	line-height: 1.2;
    text-align: left;
	color: #222
		
}

.resultstats{
	color : #808080;
}
.s{
	color: #545454;
}
.st{
	line-height: 1.4;
    word-wrap: break-word;
}

</style>
	</head> 
	

<body bgcolor="#F5DEB3"> 

<form action="result1.php" method="get"> 
		
		<span><b>Write your Keyword:</b></span>
		
		<input type="text" name="user_query" size="120"/> 
		<input type="submit" name="search" value="Search Now">
</form>
	<a href="search.html"><button>Go Back</button></a>

<?php 
	mysql_connect("localhost","root","");
	mysql_select_db("search_project2");
	function show($get_value){
		$queries = preg_split('/[, - : ; + ! @ # $ ^ & * . " \' { } | ]/', $get_value);
		
		exec("project2\search_engine\dist\process.exe $get_value" ,$output,$status);
		
		$final_time = end($output);
		
		array_pop($output);
	if($status==1){
		echo ("<center><b>Oops! sorry, nothing was found in the database!</b></center>");
		exit();
	}
	$total = count($output);
	echo "<div class = 'resultstats results'>About $total results($final_time sec)</div>";
	
	foreach($output as $filename){
	
	
	$result_query = "select * from files where filename = '$filename'";
	$run_result = mysql_query($result_query);
	
	while($row_result=mysql_fetch_array($run_result)){	
		$site_link=$row_result['filename'];
		$site_desc=$row_result['contents'];
		foreach($queries as $query){
			$site_desc = str_ireplace($query, "<strong><b>$query</b></strong>", $site_desc);
		}
	
	echo "
	
	<div class='results'>
		
		
		<a href='$site_link' target='_blank'>$site_link</a>
		<div class = 's'>
		<span class = 'st'>
		<p align='justify'>$site_desc</p>
		</span>
		</div> 
		
		
		</div>";

		}
	 }
		
	}
	function process_query($get_value){
		if($get_value==''){
	
		echo "<center><b>Please go back, and write something in the search box!</b></center>";
		exit();
	}
	show($get_value);
		
	}
	function process_voice($get_value){
		$get_value = implode(" ",$get_value);
		if($get_value==''){
	
	echo "<center><b>Please go back, and write something in the search box!</b></center>";
	exit();
	}
		show($get_value);
}
		
	
	
	if(isset($_GET['search_voice'])){
		
		exec("C:\Python34\python search_voice.py" ,$output,$status);
		
			
		if($status == 1){
			echo "<center><b>Oops! could not understand audio!</b></center>";
			exit();
		}elseif($status == 2){
			echo "<center><b>sorry! could not connect to server!Please search by typing query</b></center>";
			exit();
		}else{
			process_voice($output);
		}
		
	}
	if(isset($_GET['search'])){
	
	$get_value = $_GET['user_query'];
	process_query($get_value);
	
}


?>


</body> 
</html>