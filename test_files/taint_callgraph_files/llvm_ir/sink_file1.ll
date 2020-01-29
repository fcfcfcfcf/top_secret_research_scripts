; ModuleID = 'src/sink_file1.cpp'
source_filename = "src/sink_file1.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%class.sink_file1 = type { i8 }

@_ZN10sink_file1C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN10sink_file1C2Ev

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file1C2Ev(%class.sink_file1* %this) unnamed_addr #0 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline optnone uwtable
define dso_local i32 @_ZN10sink_file125calculate_important_valueEv() #1 align 2 {
entry:
  %call = call i32 @_ZN11taint_file117get_tainted_valueEv()
  %mul = mul nsw i32 5, %call
  %call1 = call i32 @_ZN11taint_file217get_tainted_valueEv()
  %add = add nsw i32 %mul, %call1
  ret i32 %add
}

declare dso_local i32 @_ZN11taint_file117get_tainted_valueEv() #2

declare dso_local i32 @_ZN11taint_file217get_tainted_valueEv() #2

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file121consume_tainted_valueEi(i32 %tainted_value) #0 align 2 {
entry:
  %tainted_value.addr = alloca i32, align 4
  %new_tainted_value = alloca i32, align 4
  store i32 %tainted_value, i32* %tainted_value.addr, align 4
  %0 = load i32, i32* %tainted_value.addr, align 4
  %add = add nsw i32 %0, 5
  store i32 %add, i32* %new_tainted_value, align 4
  ret void
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 9.0.1 (https://github.com/llvm/llvm-project.git 686a8891ca57463ec0d2f3ae4f732e6259cedc33)"}
