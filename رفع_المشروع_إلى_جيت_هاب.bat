@echo off
chcp 65001 > nul
title رفع مشروع أيرو فريت كينيتك إلى جيت هاب
color 0B
cls
echo ================================================================
echo      أداة رفع مشروع AR AeroFret: Kinetic إلى جيت هاب تلقائياً
echo      المطور والمهندس: محمود لبيب (Mahmoud Labib)
echo ================================================================
echo.
set DEFAULT_URL=https://github.com/mahmoudmma667-gif/-..git
echo [الرابط الافتراضي الجاهز]: %DEFAULT_URL%
echo.
set /p REPO_URL="اضغط Enter فوراً للمتابعة بالرابط أعلاه (أو الصق رابط جديد): "

if "%REPO_URL%"=="" (
    set REPO_URL=%DEFAULT_URL%
)

echo.
echo [1/3] جاري ربط المستودع البعيد origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] التأكد من فرع main...
git branch -M main

echo [3/3] جاري رفع كافة ملفات المشروع والصور والأصول إلى جيت هاب...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ================================================================
    echo   تم الرفع بنجاح تام! مشروعك الآن مباشر ومتاح للعالم على جيت هاب!
    echo ================================================================
) else (
    echo.
    echo [تنبيه] إذا ظهرت لك نافذة تسجيل الدخول إلى جيت هاب في المتصفح،
    echo         يرجى الضغط على تأكيد (Authorize) لإكمال الرفع.
)

echo.
pause
