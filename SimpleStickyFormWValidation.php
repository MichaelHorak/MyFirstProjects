<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Let's see what will happen</title>

</head>
<body>



<?php
$last_name = $first_name = $first_name_error = $last_name_error = "";
$output_form = false;
$first_name_check = true;
$last_name_check = true;

if (isset($_POST['submit'])) {
    $first_name = filter_input(INPUT_POST, 'first_name');
    $last_name = filter_input(INPUT_POST, 'last_name');


    if(empty($first_name)) {
        $first_name_error = "Please insert your first name";
        $first_name_check = false;
    }

    if(empty($last_name)) {
        $last_name_error = "Please insert your last name";
        $last_name_check = false;
    }

    if(($first_name_check) && ($last_name_check)) {
        echo "I see, you are a hacker $first_name $last_name.";
    } else {
        $output_form = true;
    }
}
else {
    $output_form = true;
}

if ($output_form) {
    ?>
    <p><strong>Enter information and we will see what will happen.</strong></p>
    <form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
        <input placeholder="First name" id="first name" name="first name" type="text" value="<?php echo htmlspecialchars($first_name) ?>" size="30" /><br />
        <?php if(isset($first_name_error)) { ?>
            <p><?php echo $first_name_error ?></p>
        <?php } ?>
        <input placeholder="Last name" id="last name" name="last name" type="text" value="<?php echo htmlspecialchars($last_name) ?>" size="30" /><br />
        <?php if(isset($last_name_error)) { ?>
            <p><?php echo $last_name_error ?></p>
        <?php } ?>
        <input type="submit" name="submit" value="Submit" />
    </form>

    <?php
}
?>

</body>
</html>