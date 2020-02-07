; ModuleID = 'src/taint_file1.cpp'
source_filename = "src/taint_file1.cpp"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%class.taint_file1 = type { i8 }

@_ZN11taint_file1C1Ev = dso_local unnamed_addr alias void (%class.taint_file1*), void (%class.taint_file1*)* @_ZN11taint_file1C2Ev

; Function Attrs: noinline nounwind optnone uwtable
define dso_local void @_ZN11taint_file1C2Ev(%class.taint_file1* %this) unnamed_addr #0 align 2 {
entry:
  %this.addr = alloca %class.taint_file1*, align 8
  store %class.taint_file1* %this, %class.taint_file1** %this.addr, align 8
  %this1 = load %class.taint_file1*, %class.taint_file1** %this.addr, align 8
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @_ZN11taint_file117get_tainted_valueEv() #0 align 2 {
entry:
  ret i32 3
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0 (https://github.com/llvm/llvm-project.git c9081968ead183ee1df824f7b96fcafcfcbe57cd)"}
