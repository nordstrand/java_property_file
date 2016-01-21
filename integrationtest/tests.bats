#!/usr/bin/env bats/bats

@test "ansible should report changed=false when no change is done" {
  run ansible --module-path=../library/ -m java_property_file -a "dest=$(pwd)/test.properties option=key value=neje" localhost 
  [ "$status" -eq 0 ]
  [[ $output =~ SUCCESS ]]
  [[ $output =~ "\"changed\": true" ]]

  run ansible --module-path=../library/ -m java_property_file -a "dest=$(pwd)/test.properties option=key value=neje" localhost 
  [ "$status" -eq 0 ]
  [[ $output =~ SUCCESS ]]
  [[ $output =~ "\"changed\": false" ]]
}
