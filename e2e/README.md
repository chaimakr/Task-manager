# End 2 End Tests
- I used Selenium and wrote 6 e2e test , the scenario treated is :
  - visiting home page Signing up a new user "e2e tester" 
  - then signing in with root user (it's a user auto created with database)
  - checking user home page after login
  - adding a new task
  - updating the state of a task
  - deleting the task
  - logout

__A database teste2e.db is created at the start of the test and removed at the end of it__
### Test Execution: 
<p align="center">
    <img src="./static/img/e2e OK.PNG" alt="End 2 End execution">
</p>

Side note: I used webdriver-manager locally to dynamically install chrome driver depending on the browser version we're testing on, 
but it made some conflicts in the pipeline so I switched to a static driver which does not work locally but runs perfectly in the pipeline :
<br>
```
#inst.driver = webdriver.Chrome(ChromeDriverManager().install()) 
inst.driver = webdriver.Chrome(options = chrome_options)
```
