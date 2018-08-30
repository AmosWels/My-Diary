## My Diary 
MyDiary is an online journal where users can pen down their thoughts and feelings.

[![Build Status](https://travis-ci.org/AmosWels/My-Diary.svg?branch=database)](https://travis-ci.org/AmosWels/My-Diary)

[![Coverage Status](https://coveralls.io/repos/github/AmosWels/My-Diary/badge.svg?branch=chal4)](https://coveralls.io/github/AmosWels/My-Diary?branch=chal4)

<a href="https://codeclimate.com/github/AmosWels/My-Diary/maintainability"><img src="https://api.codeclimate.com/v1/badges/911827d24f11c39cdf13/maintainability" /></a>

#### [Visit my diario Documentation](https://mydiario.docs.apiary.io/#introduction/mydiario-requests-collection/get-all-users-entries-[get/entries])

#### [Visit my diario at gh-pages](https://amoswels.github.io/My-Diary/UI/)

#### Required Features
1. Create user accounts that can signin/signout from the app. 
2. Get all diary entries for a particular user.
3. Get a specific diary entry for a particular user.
4. Add an entry
5. Modify an entry.

#### Endpoints

POST /api/v1/auth/signup
Register a user

POST /api/v1/auth/login
Login a user

GET /api/v1/entries 
Fetch all the entries for a user.

GET /api/v1/entries/<entryId>
Fetch the details of an entry for a user

POST /api/v1/entries
Add an entry

PUT /api/v1/entries/<entryId>
Modify a diary entry
An entry can only be modified on the same day it was created.

GET /api/v1/authuser
Fetch details of signed in user

POST /api/v1/authuser/profile
Add profile of signed in user to enable notifications

GET /api/v1/authuser/profile
Fetch full profile details of user

PUT /api/v1/authuser/profile
Modify the profile of a user

##### Prerequisites
Requiremets to run this My Diary
1. Server side Framework: ​Flask Python Framework
2. Testing Framework: PyTest

##### You can clone with [git clone -url-]
url = https://github.com/AmosWels/My-Diary.git
