module Progress exposing (Progress, decode)

import Dict exposing (Dict)
import Experiment exposing (Experiment)
import Json.Decode


{-| A currently running experiment on the server.
-}
type alias Progress =
    { experiment : Experiment
    , directory : String
    , currentPhase : String
    , currentPlugin : String
    , currentUpdate : Int
    , totalUpdates : Int
    , updateTime : Float
    , pluginProgress : Dict String Json.Decode.Value
    }


decode : Json.Decode.Decoder Progress
decode =
    Json.Decode.map8
        Progress
        (Json.Decode.field "experiment" Experiment.decode)
        (Json.Decode.field "directory" Json.Decode.string)
        (Json.Decode.field "current_phase" Json.Decode.string)
        (Json.Decode.field "current_plugin" Json.Decode.string)
        (Json.Decode.field "current_update" Json.Decode.int)
        (Json.Decode.field "total_updates" Json.Decode.int)
        (Json.Decode.field "update_time" Json.Decode.float)
        (Json.Decode.field "plugin" <| Json.Decode.dict Json.Decode.value)
