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
; >>> (define identity (lambda (x) (* x x)))
; >>> (map-reverse identity '(4 3 2 1))
; (1 4 9 16)
;;;
(define (map-reverse proc items)  ; > (+ 3 1) => 1  ; wrong!
  (if (null? items)  ; > (define a 1) => a  ; also a test!
    nil
    (append (map-reverse proc (cdr items)) (list (proc (car items)))))
)
