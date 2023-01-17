<?php
$country_list = array("", "Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra",
    "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia",
    "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
    "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
    "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory",
    "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon",
    "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile",
    "China", "Christmas Island", "Cocos Islands", "Colombia", "Comoros", "Congo",
    "Democratic Republic of the Congo", "Cook Islands", "Costa Rica", "Cote d'Ivoire",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
    "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands",
    "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana",
    "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany",
    "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands",
    "Holy See", "Honduras", "Hong Kong", "Hungary", "Iceland", "India",
    "Indonesia", "Islamic Republic of Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Democratic People's Republic of Korea",
    "Republic of Korea", "Kuwait", "Kyrgyzstan", "People's Democratic Republic Lao", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Macau", "The Former Yugoslav Republic of Macedonia", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania",
    "Mauritius", "Mayotte", "Mexico", "Federated States of Micronesia", "Republic of Moldova",
    "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman",
    "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania",
    "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands",
    "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname",
    "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic",
    "Taiwan, Province of China", "Tajikistan", "United Republic of Tanzania", "Thailand", "Togo",
    "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom", "United States", "United States Minor Outlying Islands", "Uruguay",
    "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands", "Wallis and Futuna Islands",
    "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe");

$first_name = $country = $first_name_error = $country_error = "";
$output_form = false;
$first_name_check = true;
$country_check = true;

if (isset($_POST['submit'])) {
    $first_name = filter_input(INPUT_POST, 'first_name');
    $country = filter_input(INPUT_POST, 'country');

    if(empty($first_name)) {
        $first_name_error = "Please insert your first name";
        $first_name_check = false;
    }

    if(empty($country)) {
        $country_error = "Please select a country";
        $country_check = false;
    }

    if(($first_name_check)&&($country_check)) {
        echo "$first_name is from $country";
    } else {
        $output_form = true;
    }
}
else {
    $output_form = true;
}

if ($output_form) {
?>
<form method="post" action="<?php echo $_SERVER['PHP_SELF']; ?>">
    <input placeholder="First name" type="text" id="first name" name="first name"
           value="<?php echo htmlspecialchars($first_name)?>"/>
    <?php if(isset($first_name_error)) { ?>
        <span><?php echo $first_name_error ?></span>
    <?php } ?><br /><br />

    <select name="country" id="country" required>
        <?php
        for($i=0; $i<239; $i++) {
            echo "<option value='$country_list[$i]'";
            if($country_list[$i]==$country) { echo "selected";}
            echo ">$country_list[$i]</option>";
        } ?>
        </select>
    <input type="submit" value="Generate response" name="submit" />
</form>
<?php
}
?>
