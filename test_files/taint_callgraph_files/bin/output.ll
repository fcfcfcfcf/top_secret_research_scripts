; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%class.sink_file1 = type { i8 }

@_ZN10sink_file1C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN10sink_file1C2Ev
@_ZN10sink_file2C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN10sink_file2C2Ev
@_ZN10sink_file3C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN10sink_file3C2Ev
@_ZN11taint_file1C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN11taint_file1C2Ev
@_ZN11taint_file2C1Ev = dso_local unnamed_addr alias void (%class.sink_file1*), void (%class.sink_file1*)* @_ZN11taint_file2C2Ev

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

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file1C2Ev(%class.sink_file1* %this) unnamed_addr #1 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline optnone uwtable
define dso_local i32 @_ZN10sink_file125calculate_important_valueEv() #2 align 2 {
entry:
  %call = call i32 @_ZN11taint_file117get_tainted_valueEv()
  %mul = mul nsw i32 5, %call
  %call1 = call i32 @_ZN11taint_file217get_tainted_valueEv()
  %add = add nsw i32 %mul, %call1
  ret i32 %add
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file121consume_tainted_valueEi(i32 %tainted_value) #1 align 2 {
entry:
  %tainted_value.addr = alloca i32, align 4
  %new_tainted_value = alloca i32, align 4
  store i32 %tainted_value, i32* %tainted_value.addr, align 4
  %0 = load i32, i32* %tainted_value.addr, align 4
  %add = add nsw i32 %0, 5
  store i32 %add, i32* %new_tainted_value, align 4
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file2C2Ev(%class.sink_file1* %this) unnamed_addr #3 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline optnone uwtable
define dso_local i32 @_ZN10sink_file225calculate_important_valueEv() #4 align 2 {
entry:
  %call = call i32 @_ZN11taint_file117get_tainted_valueEv()
  %mul = mul nsw i32 2, %call
  ret i32 %mul
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN10sink_file3C2Ev(%class.sink_file1* %this) unnamed_addr #3 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @_ZN10sink_file325calculate_important_valueEv() #3 align 2 {
entry:
  ret i32 2
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN11taint_file1C2Ev(%class.sink_file1* %this) unnamed_addr #3 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @_ZN11taint_file117get_tainted_valueEv() #3 align 2 {
entry:
  ret i32 3
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN11taint_file2C2Ev(%class.sink_file1* %this) unnamed_addr #3 align 2 {
entry:
  %this.addr = alloca %class.sink_file1*, align 8
  store %class.sink_file1* %this, %class.sink_file1** %this.addr, align 8
  %this1 = load %class.sink_file1*, %class.sink_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @_ZN11taint_file217get_tainted_valueEv() #3 align 2 {
entry:
  ret i32 2
}

attributes #0 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0, !0, !1, !1, !1, !1}
!llvm.module.flags = !{!2}

!0 = !{!"clang version 9.0.1 (https://github.com/llvm/llvm-project.git 686a8891ca57463ec0d2f3ae4f732e6259cedc33)"}
!1 = !{!"clang version 10.0.0 (https://github.com/llvm/llvm-project.git c9081968ead183ee1df824f7b96fcafcfcbe57cd)"}
!2 = !{i32 1, !"wchar_size", i32 4}
