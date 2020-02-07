; ModuleID = 'src/main.cpp'
source_filename = "src/main.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main() #0 {
entry:
  %retval = alloca i32, align 4
  %tainted_data = alloca i32, align 4
  store i32 0, i32* %retval, align 4
  %call = call i32 @_ZN10sink_file125calculate_important_valueEv()
  %call1 = call i32 @_ZN10sink_file225calculate_important_valueEv()
  %call2 = call i32 @_ZN10sink_file325calculate_important_valueEv()
  %call3 = call i32 @_ZN11taint_file117get_tainted_valueEv()
  store i32 %call3, i32* %tainted_data, align 4
  %0 = load i32, i32* %tainted_data, align 4
  call void @_ZN10sink_file121consume_tainted_valueEi(i32 %0)
  ret i32 0
}

declare dso_local i32 @_ZN10sink_file125calculate_important_valueEv() #1

declare dso_local i32 @_ZN10sink_file225calculate_important_valueEv() #1

declare dso_local i32 @_ZN10sink_file325calculate_important_valueEv() #1

declare dso_local i32 @_ZN11taint_file117get_tainted_valueEv() #1

declare dso_local void @_ZN10sink_file121consume_tainted_valueEi(i32) #1

attributes #0 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 9.0.1 (https://github.com/llvm/llvm-project.git 686a8891ca57463ec0d2f3ae4f732e6259cedc33)"}
