# Common XSS patterns to detect potential cross-site scripting vulnerabilities
XSS_PATTERNS = [
    # Direct output of GET/POST/REQUEST/COOKIE variables
    r'echo\s*\$_(GET|POST|REQUEST|COOKIE)\[.*\];',
    r'print\s*\$_(GET|POST|REQUEST|COOKIE)\[.*\];',
    r'\$_(GET|POST|REQUEST|COOKIE)\[.*\]\s*;',
    
    # Output of general PHP variables
    r'echo\s*\$\w+\s*;',
    r'print\s*\$\w+\s*;',
    
    # Output of methods or properties within classes
    r'echo\s*\$this->\w+\(\s*\)\s*;',#esc_attr(echo())
    r'print\s*\$this->\w+\(\s*\)\s*;',
    
    # Output of methods or properties within HTML attributes
    r'value="\s*<?php\s*echo\s*\$this->\w+\(\s*\)\s*;?\s*?>"',
    r'value="\s*<?php\s*print\s*\$this->\w+\(\s*\)\s*;?\s*?>"',
    
    # Users can add thier own patterns here
]

# Patterns to detect common sanitization functions that may indicate false positives
SANITIZATION_PATTERNS = [
    r'esc_attr\(',       # Detect usage of esc_attr() function
    r'esc_html\(',       # Detect usage of esc_html() function
    # r'sanitize_text_field\(',  # Detect usage of sanitize_text_field() function
    r'htmlspecialchars\(', # Detect usage of htmlspecialchars() function
    r'\(int\)\s*\$_(GET|POST|REQUEST|COOKIE)\[.*\]', # Detect casting to integer
    r'intval\(',         # Detect usage of intval() function
    r'filter_var\(\s*\$_(GET|POST|REQUEST|COOKIE)\[.*\],\s*FILTER_SANITIZE_NUMBER_INT\s*\)', # Detect usage of filter_var with FILTER_SANITIZE_NUMBER_INT
    # Add more sanitization functions if needed
]

# Common SQL Injection patterns to detect potential SQL injection vulnerabilities
SQLI_PATTERNS = [
    # Basic SQL query pattern with potential user input
    r"SELECT \* FROM users WHERE id = '\d+'",
    
    # Variable assignment with user input and use in SQL query (mysql_query)
    r"\$.*=.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\];.*\bmysql_query\b.*\$\w+",
    
    # Variable assignment with user input and use in SQL query (mysqli_query)
    r"\$.*=.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\];.*\bmysqli_query\b.*\$\w+",
    
    # Variable assignment with user input and use in SQL query (PDO query)
    r"\$.*=.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\];.*\bPDO\b.*\bquery\b.*\$\w+",
    
    # Direct inclusion of user input in SQL queries (mysql_query, mysqli_query, PDO query)
    r"\bmysql_query\b\(['\"].*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*['\"].*\);",
    r"\bmysqli_query\b\(['\"].*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*['\"].*\);",
    r"\bPDO\b.*->query\(['\"].*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*['\"].*\);",
    
    # Variable use directly in SQL queries (mysql_query, mysqli_query, PDO query)
    r"\bmysql_query\b\(\$.*\);",
    r"\bmysqli_query\b\(\$.*\);",
    r"\bPDO\b.*->query\(\$.*\);",
    
    # General user input in SQL queries (mysql_query, mysqli_query, PDO query)
    r"\bmysql_query\b\(['\"].*\$_(GET|POST|REQUEST|COOKIE).*['\"].*\);",
    r"\bmysqli_query\b\(['\"].*\$_(GET|POST|REQUEST|COOKIE).*['\"].*\);",
    r"\bPDO\b.*->query\(['\"].*\$_(GET|POST|REQUEST|COOKIE).*['\"].*\);",
    
    # Use of concatenation with user input in SQL queries (mysql_query, mysqli_query, PDO query)
    r"\bmysql_query\b\(.*concat\(\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*\);",
    r"\bmysqli_query\b\(.*concat\(\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*\);",
    r"\bPDO\b.*->query\(.*concat\(\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*\);",
    
    # Indirect user input in SQL queries (mysql_query, mysqli_query, PDO query)
    r"\$.*\s?=\s?.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*;\s*\$.*\bmysql_query\b\(.*\$\w+.*\);",
    r"\$.*\s?=\s?.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*;\s*\$.*\bmysqli_query\b\(.*\$\w+.*\);",
    r"\$.*\s?=\s?.*\$_(GET|POST|REQUEST|COOKIE)\['[^\]]+'\].*;\s*\$.*\bPDO\b.*->query\(.*\$\w+.*\);",
    
    # Direct use of variables in DB::select() method
    r"\bDB::select\b\s*\(\s*\bDB::raw\b\s*\(\s*['\"].*\$\w+.*['\"].*\)\s*\);",
    
    # Add more SQL patterns here

    # Direct concatenation of user input in SQL queries
    r'\$.*=.*\$_(GET|POST|REQUEST|COOKIE)\[.*\];.*\b(?:mysql_query|mysqli_query|PDO::query|wpdb->query)\b\(',
    
    # Variable assignment with user input used in SQL queries
    r'\$.*=.*\$_(GET|POST|REQUEST|COOKIE)\[.*\];.*\b(?:mysql_query|mysqli_query|PDO::query|wpdb->query)\b\(\$.*\);',
    
    # Direct inclusion of unsanitized user input in SQL queries
    r"\b(?:mysql_query|mysqli_query|PDO::query|wpdb->query)\b\(['\"].*\$_(GET|POST|REQUEST|COOKIE)\[.*\].*['\"].*\);",
    
    # Concatenation of user input in SQL queries
    r'\b(?:mysql_query|mysqli_query|PDO::query|wpdb->query)\b\(\s*["\'].*\+\s*\$_(GET|POST|REQUEST|COOKIE)\[.*\].*\+\s*["\'].*\);',
    
    # Variable directly used in SQL queries
    r'\b(?:mysql_query|mysqli_query|PDO::query|wpdb->query)\b\(\s*\$.*\);',
    
]

CUSTOM_PATTERNS = [

    r'function\s+handle_upload_file\s*\(.*\)\s*{',
    #To find the pattern : "public function handle_upload_file( $file ) {"
    r'end_redirect_link'
    
    #user can add thier own custom pattern based on thier experience

]