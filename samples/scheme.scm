;;;
; Expect Utility
; --------------
;
; Regardless of comment type, all tests in this file will be detected. We will
; demonstrate that expect can handle several edge cases, accommodate regular
; doctest formats, and detect inline tests.
;
; >>> (* 2 2)
; 4
; >>> (+ 3 5)  ; comments
; 8
; >>> (+ 6 3)  ; wrong!
; 5
;;;


;;;
; Maps procedure over all items but returns results in reverse order
;
; >>> (map-reverse (lambda (x) (* x x))) '(4 3 2 1))
; (1 4 9 16)
;;;
(define (map-reverse proc items)  ; > (+ 3 1) ; wrong! => 1
  (if (null? items)  ; > (define a 1) ; place comments after test input =>
    ()
    (append (map-reverse proc (cdr items)) (list (proc (car items)))))
)
