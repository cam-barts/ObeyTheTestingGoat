# The [To Do App](http://camstodo.ddns.net) To End All To Do Apps

[![Build Status](https://travis-ci.com/cam-barts/ObeyTheTestingGoat.svg?branch=master)](https://travis-ci.com/cam-barts/ObeyTheTestingGoat)

#### Based on Harry Percival's [Test-Driven Development with Python](https://www.amazon.com/Test-Driven-Development-Python-Selenium-JavaScript/dp/1491958707/)

* Hosted on an [Azure](portal.azure.com) VM
* Host name provided my [NoIP](https://www.noip.com/)


#### Interesting CI/CD Notes
  ##### Current
 * CI with [Travis](https://travis-ci.com/cam-barts/ObeyTheTestingGoat) for the sweet badge
 * CI/CD  on [Visual Studio Team Services](https://cambarts.visualstudio.com/TestToDo/) Pipeline as Follows
      1. Push project to Github
      2. VSTS Pulls Project
      3. Run Unittests
      4. If Unittest Pass, deploy to staging site using [Fabric](www.fabfile.org)


  ##### Future
  * Run Functional Tests On Staging Site
  * If Functional Tests Pass, deploy to [Live Site](camstodo.ddns.net)
