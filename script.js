document.addEventListener('DOMContentLoaded', function() {
    const suggestionForm = document.getElementById('suggestionForm');

    if (suggestionForm) {
        suggestionForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const nameInput = document.getElementById('name').value;
            const suggestionInput = document.getElementById('suggestion').value;
            const messageStatus = document.getElementById('messageStatus');

            // إظهار رسالة "جاري الإرسال..." للمخدم
            messageStatus.textContent = "جاري إرسال اقتراحك المتميز .. ✨";
            messageStatus.style.color = "#333";
            messageStatus.style.display = "block";

            // إرسال البيانات إلى سيرفر البايثون المحلي مع تحديد وضع CORS صراحةً
            fetch('http://127.0.0.1:8000/submit-suggestion', {
                method: 'POST',
                mode: 'cors', // تأكيد وضع CORS للالتفاف حول حظر الحماية
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: nameInput,
                    suggestion: suggestionInput
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    messageStatus.textContent = "تم إرسال اقتراحك بنجاح! شكراً لكِ. 📥";
                    messageStatus.style.color = "#2A5647"; // نستخدم الأخضر الخاص بالهوية للنجاح
                    suggestionForm.reset(); // تفريغ الحقول بعد النجاح
                } else {
                    messageStatus.textContent = "عذراً، حدثت مشكلة أثناء الإرسال. ❌";
                    messageStatus.style.color = "red";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageStatus.textContent = "لم يتم الاتصال بالسيرفر. تأكدي أن ملف البايثون يعمل! 🔌";
                messageStatus.style.color = "red";
            });
        });
    } else {
        console.error('تحذير: لم يتم العثور على النموذج "suggestionForm" في صفحة الـ HTML!');
    }
});