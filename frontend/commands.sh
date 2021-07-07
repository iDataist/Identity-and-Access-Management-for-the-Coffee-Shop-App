brew install angular-cli

# fix error "An unhandled exception occurred: Cannot read property 'Minus' of undefined"
ng update @angular/cli @angular/core --allow-dirty --force

# fix error "Schema validation failed with the following errors: Data path "" must NOT have additional properties(es5BrowserSupport)."
# removed "es5BrowserSupport": true from angular.json