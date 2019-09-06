if exist chrome ( rmdir /q /s chrome )
if exist firefox ( rmdir /q /s firefox )
if exist %temp%\ckan_ui_test ( rmdir /q /s %temp%\ckan_ui_test )
mkdir %temp%\ckan_ui_test
virtualenv %temp%\ckan_ui_test --python=3.6
call %temp%\ckan_ui_test\Scripts\activate
pip install -r .\requirement.txt
tox
deactivate
if exist .tox ( rmdir /q /s .tox )
